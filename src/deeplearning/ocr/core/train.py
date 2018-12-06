# -*- coding:utf-8 -*-
"""
@File      : train.py
@Software  : OCR
@Time      : 2018/3/30 17:22
@Author    : yubb
"""
import os
import numpy as np
import tensorflow as tf
import ops.inception_v3 as network
from data.dataset import TextDataSet, load_data

tf.app.flags.DEFINE_float('margin', 0.3, "*margin.")
tf.app.flags.DEFINE_integer('batch_size', 100, "*batch size.")
tf.app.flags.DEFINE_integer('examples_num', 3, "*examples num.")
tf.app.flags.DEFINE_string('model_name', 'model.ckpt', "*Name of model.")
tf.app.flags.DEFINE_string('dest', './data', "*Location of dataset.")
tf.app.flags.DEFINE_string('model_save_path', '../../resources/model', "*model save path.")
tf.app.flags.DEFINE_float('regularization_rate', 0.0001, "*regularization rate.")
tf.app.flags.DEFINE_float('moving_average_decay', 0.99, "*moving average decay.")
tf.app.flags.DEFINE_float('learning_rate_base', 0.8, "*learning rate base.")
tf.app.flags.DEFINE_float('learning_rate_decay', 0.99, "*learning rate decay.")
tf.app.flags.DEFINE_integer('embeddings_size', 128, "*examples num.")
FLAGS = tf.app.flags.FLAGS


def train():
    dataset = TextDataSet(FLAGS.dest)
    episodes = dataset.dataset_size // FLAGS.batch_size

    image_placeholder = tf.placeholder(tf.float32, [FLAGS.examples_num,
                                                    network.IMAGE_SIZE,
                                                    network.IMAGE_SIZE,
                                                    network.NUM_CHANNELS], name='image_placeholder')

    # regularizer = tf.contrib.layers.l2_regularizer(FLAGS.regularization_rate)
    # prelogits = network.inference(image_placeholder, is_training=True, regularizer=regularizer)

    prelogits, _ = network.inference(image_placeholder, is_training=False)
    embeddings = tf.nn.l2_normalize(prelogits, 1, 1e-10, name='embeddings')
    anchor, positive, negative = tf.unstack(tf.reshape(embeddings, [-1, 3, FLAGS.embeddings_size]), 3, 1)

    # 滑动平均
    global_step = tf.Variable(0, trainable=False)
    variable_averages = tf.train.ExponentialMovingAverage(FLAGS.moving_average_decay, global_step)
    variable_averages_op = variable_averages.apply(tf.trainable_variables())
    learning_rate = tf.train.exponential_decay(FLAGS.learning_rate_base, global_step, episodes,
                                               FLAGS.learning_rate_decay)

    # 计算loss
    triplet_loss = network.triplet_loss(anchor, positive, negative, FLAGS.margin)
    regularization_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
    total_loss = tf.add_n([triplet_loss] + regularization_losses, name='total_loss')
    tf.summary.scalar('total_loss', total_loss)

    # 计算梯度
    opt = tf.train.AdagradOptimizer(learning_rate)
    grads = opt.compute_gradients(total_loss, tf.global_variables())
    apply_gradient_op = opt.apply_gradients(grads, global_step=global_step)

    with tf.control_dependencies([apply_gradient_op, variable_averages_op]):
        train_op = tf.no_op(name='train')

    saver = tf.train.Saver()

    with tf.Session() as sess:
        summary_writer = tf.summary.FileWriter('./tmp/views/', sess.graph)
        sess.run(tf.global_variables_initializer())
        model_path = os.path.join(FLAGS.model_save_path, 'checkpoint')
        if os.path.exists(model_path):
            ckpt = tf.train.get_checkpoint_state(FLAGS.model_save_path)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, os.path.expanduser(ckpt.model_checkpoint_path))
                image_placeholder = tf.get_default_graph().get_tensor_by_name("image_placeholder:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                from data.dataset import load_embs_data
                files, labels = load_embs_data(FLAGS.dest)
                emb_array = np.zeros((len(files), FLAGS.embeddings_size))
                for idx in range(0, len(files), 3):
                    batch = load_data(files[idx:idx + 3])
                    data = np.reshape(batch, (FLAGS.examples_num, network.IMAGE_SIZE,
                                              network.IMAGE_SIZE, network.NUM_CHANNELS))
                    embs = sess.run(embeddings, feed_dict={image_placeholder: data})
                    emb_array[idx, :], emb_array[idx + 1, :], emb_array[idx + 2, :] = embs[0, :], embs[1, :], embs[2, :]
                batch = load_data(['./data/安/2.png', './data/安/0.png', './data/安/0.png'])
                data = np.reshape(batch, (FLAGS.examples_num, network.IMAGE_SIZE,
                                          network.IMAGE_SIZE, network.NUM_CHANNELS))
                embs = sess.run(embeddings, feed_dict={image_placeholder: data})
                # dist = np.sqrt(np.sum(np.square(np.subtract(embs[0, :], embs[1, :]))))
                goal = np.array([embs[0, :] for i in range(emb_array.shape[0])])
                dists = np.sqrt(np.sum(np.square(np.subtract(goal, emb_array)), axis=1))
                indexes = np.where(dists == np.min(dists))
                print("Word IN Image: {}".format([labels[i] for i in indexes[0]]))
                quit()
        for step in range(episodes):
            imgs, paths, labels = dataset.next_batch(FLAGS.batch_size)
            train_operation(sess, summary_writer, global_step, imgs, paths, labels, image_placeholder, train_op,
                            embeddings, total_loss)
        saver.save(sess, model_path, global_step=global_step)


def train_operation(sess, summary_writer, global_step, imgs, paths, labels, image_placeholder, train_op, embeddings,
                    total_loss):
    np.random.shuffle(imgs)
    emb_array = np.zeros((len(imgs) * len(imgs[0]), FLAGS.embeddings_size))
    for idx in range(len(imgs)):
        batch = load_data(imgs[idx])
        data = np.reshape(batch, (FLAGS.examples_num, network.IMAGE_SIZE,
                                  network.IMAGE_SIZE, network.NUM_CHANNELS))
        emb = sess.run([embeddings], feed_dict={image_placeholder: data})
        emb_array[idx * 3, :] = emb[0][0]
        emb_array[idx * 3 + 1, :] = emb[0][1]
        emb_array[idx * 3 + 2, :] = emb[0][2]
    triplets = select_triplets(emb_array, paths, FLAGS.margin)
    summary = tf.Summary()
    for triplet in triplets:
        batch = load_data(triplet)
        data = np.reshape(batch, (FLAGS.examples_num, network.IMAGE_SIZE,
                                  network.IMAGE_SIZE, network.NUM_CHANNELS))
        loss, _, emb, step = sess.run([total_loss, train_op, embeddings, global_step],
                                      feed_dict={image_placeholder: data})
        print("After {} step: loss={}".format(step, loss))
        summary.value.add(tag='loss', simple_value=loss)
        summary_writer.add_summary(summary, step)


def select_triplets(emb_array, image_paths, alpha, sample_num=3):
    triplets = []
    for idx in range(0, emb_array.shape[0], 3):
        for i in range(sample_num):
            a_idx = idx + i
            total_dists = np.sum(np.square(emb_array[a_idx] - emb_array), 1)
            for j in range(i + 1, sample_num):
                p_idx = idx + j
                pos_dist = np.sum(np.square(emb_array[a_idx] - emb_array[p_idx]))
                total_dists[idx:idx + sample_num] = np.NaN
                all_neg = np.where(total_dists - pos_dist < alpha)[0]
                rnd_negs = all_neg.shape[0]
                if rnd_negs > 0:
                    rnd_idx = np.random.randint(rnd_negs)
                    n_idx = all_neg[rnd_idx]
                    triplets.append([image_paths[a_idx], image_paths[p_idx], image_paths[n_idx]])
    return triplets


def evaluate():
    saver = tf.train.Saver()
    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state('./data')
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)


def test():
    data = np.random.rand(35 * 35 * 3).astype(np.float32).reshape((3, 35, 35, 1))
    import ops.inception_v3 as inception_v3
    rs = inception_v3.inference(data)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(rs))


def main(argv=None):
    train()
    # evaluate()


if __name__ == '__main__':
    tf.app.run()
