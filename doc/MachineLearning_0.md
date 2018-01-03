# ML:Introduction
## What is Machine Learning?
>Two definitions of Machine Learning are offered. Arthur Samuel described it as: "the field of study that gives computers the ability to learn without being explicitly programmed." This is an older, informal definition.

>Tom Mitchell provides a more modern definition: "A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P, if its performance at tasks in T, as measured by P, improves with experience E."

>Example: playing checkers.

>E = the experience of playing many games of checkers

>T = the task of playing checkers.

>P = the probability that the program will win the next game.

>In general, any machine learning problem can be assigned to one of two broad classifications:

>supervised learning, OR

>unsupervised learning.

### Supervised Learning
>In supervised learning, we are given a data set and already know what our correct output should look like, having the idea that there is a relationship between the input and the output.

>Supervised learning problems are categorized into "regression" and "classification" problems. In a regression problem, we are trying to predict results within a continuous output, meaning that we are trying to map input variables to some continuous function. In a classification problem, we are instead trying to predict results in a discrete output. In other words, we are trying to map input variables into discrete categories. Here is a description on Math is Fun on Continuous and Discrete Data.

### Example 1:
>Given data about the size of houses on the real estate market, try to predict their price. Price as a function of size is a continuous output, so this is a regression problem.

>We could turn this example into a classification problem by instead making our output about whether the house "sells for more or less than the asking price." Here we are classifying the houses based on price into two discrete categories.

### Example 2:

>(a) Regression - Given a picture of Male/Female, We have to predict his/her age on the basis of given picture.

>(b) Classification - Given a picture of Male/Female, We have to predict Whether He/She is of High school, College, Graduate age. Another Example for Classification - Banks have to decide whether or not to give a loan to someone on the basis of his credit history.

### Unsupervised Learning
>Unsupervised learning, on the other hand, allows us to approach problems with little or no idea what our results should look like. We can derive structure from data where we don't necessarily know the effect of the variables.

>We can derive this structure by clustering the data based on relationships among the variables in the data.

>With unsupervised learning there is no feedback based on the prediction results, i.e., there is no teacher to correct you.

### Example:
>Clustering: Take a collection of 1000 essays written on the US Economy, and find a way to automatically group these essays into a small number that are somehow similar or related by different variables, such as word frequency, sentence length, page count, and so on.

>Non-clustering: The "Cocktail Party Algorithm", which can find structure in messy data (such as the identification of individual voices and music from a mesh of sounds at a cocktail party (https://en.wikipedia.org/wiki/Cocktail_party_effect) ). Here is an answer on Quora to enhance your understanding. : https://www.quora.com/What-is-the-difference-between-supervised-and-unsupervised-learning-algorithms ?

# ML:Linear Regression with One Variable
## Model Representation
>Recall that in regression problems, we are taking input variables and trying to fit the output onto a continuous expected result function.

>Linear regression with one variable is also known as "univariate linear regression."

>Univariate linear regression is used when you want to predict a single output value y from a single input value x. We're doing supervised learning here, so that means we already have an idea about what the input/output cause and effect should be.

## The Hypothesis Function
>Our hypothesis function has the general form:

$$ 
\hat{y}=h_\theta(x)=\theta_0+\theta_1x 
$$

>Note that this is like the equation of a straight line. We give to hθ(x) values for θ0 and θ1 to get our estimated output y^. In other words, we are trying to create a function called hθ that is trying to map our input data (the x's) to our output data (the y's).
### Example:
>Suppose we have the following set of training data:

input x | output y
----|----
0   |4
1   |7
2   |7
3   |8
>Now we can make a random guess about our hθ function: θ0=2 and θ1=2. The hypothesis function becomes hθ(x)=2+2x.

>So for input of 1 to our hypothesis, y will be 4. This is off by 3. Note that we will be trying out various values of θ0 and θ1 to try to find values which provide the best possible "fit" or the most representative "straight line" through the data points mapped on the x-y plane.
# Cost Function
>We can measure the accuracy of our hypothesis function by using a cost function. This takes an average (actually a fancier version of an average) of all the results of the hypothesis with inputs from x's compared to the actual output y's.

$$ 
J(\theta_0,\theta_1)=\frac{1}{2m}\sum_{i=1}^{m}(\hat{y}_i-y_i)^2=\frac{1}{2m}\sum_{i=1}^{m}(h_\theta(x_i)-y_i)^2 
$$

>To break it apart, it is 12 x¯ where x¯ is the mean of the squares of hθ(xi)−yi , or the difference between the predicted value and the actual value.

>This function is otherwise called the "Squared error function", or "Mean squared error". The mean is halved (12m) as a convenience for the computation of the gradient descent, as the derivative term of the square function will cancel out the 12 term.

>Now we are able to concretely measure the accuracy of our predictor function against the correct results we have so that we can predict new results we don't have.

>If we try to think of it in visual terms, our training data set is scattered on the x-y plane. We are trying to make straight line (defined by hθ(x)) which passes through this scattered set of data. Our objective is to get the best possible line. The best possible line will be such so that the average squared vertical distances of the scattered points from the line will be the least. In the best case, the line should pass through all the points of our training data set. In such a case the value of J(θ0,θ1) will be 0.

# ML:Gradient Descent

>So we have our hypothesis function and we have a way of measuring how well it fits into the data. Now we need to estimate the parameters in hypothesis function. That's where gradient descent comes in.

>Imagine that we graph our hypothesis function based on its fields θ0 and θ1 (actually we are graphing the cost function as a function of the parameter estimates). This can be kind of confusing; we are moving up to a higher level of abstraction. We are not graphing x and y itself, but the parameter range of our hypothesis function and the cost resulting from selecting particular set of parameters.

>We put θ0 on the x axis and θ1 on the y axis, with the cost function on the vertical z axis. The points on our graph will be the result of the cost function using our hypothesis with those specific theta parameters.

>We will know that we have succeeded when our cost function is at the very bottom of the pits in our graph, i.e. when its value is the minimum.

>The way we do this is by taking the derivative (the tangential line to a function) of our cost function. The slope of the tangent is the derivative at that point and it will give us a direction to move towards. We make steps down the cost function in the direction with the steepest descent, and the size of each step is determined by the parameter α, which is called the learning rate.

>The gradient descent algorithm is:

>repeat until convergence: