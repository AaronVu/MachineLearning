import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.KeyGenerator;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;


public class PasswdEncode {
	
    private final static String MD5 = "MD5";

    private final static String SHA = "SHA";

    private final static String AES = "AES";

    private static String hexStr =  "0123456789ABCDEF";

    private final static String chart_set_utf8 = "UTF-8";
    
    public static final String USER_NAME_KEY = "VMEININ_NAME";
    public static final String USER_PWD_KEY = "VMEININ_PWD";

    /**
     *
     * @param bytes
     * @return  将二进制转换为十六进制字符输出
     */
    private static String bytesToHexString(byte[] bytes) {
        if(bytes== null ){
            return null;
        }
        String result = "";
        String hex = "";
        for (int i = 0; i < bytes.length; i++) {
            // 字节高4位
            hex = String.valueOf(hexStr.charAt((bytes[i] & 0xF0) >> 4));
            // 字节低4位
            hex += String.valueOf(hexStr.charAt(bytes[i] & 0x0F));
            result += hex;
        }
        return result;
    }

    /**
     *
     * @param hexString
     * @return 将十六进制转换为字节数组
     */
    public static byte[] hexStringToBytes(String hexString) {
        if(hexString == null ){
            return null;
        }
        // hexString的长度对2取整，作为bytes的长度
        int len = hexString.length() / 2;
        byte[] bytes = new byte[len];
        byte high = 0;//字节高四位
        byte low = 0;// 字节低四位

        for (int i = 0; i < len; i++) {
        	// 右移四位得到高位
            high = (byte) ((hexStr.indexOf(hexString.charAt(2 * i))) << 4);
            low = (byte) hexStr.indexOf(hexString.charAt(2 * i + 1));
            bytes[i] = (byte) (high | low);//高地位做或运算
        }
        return bytes;
    }

    /**
     * md5不可逆加密码
     * @param param
     * @return
     */
    private static byte[] MD5Encode(byte[] param){
        MessageDigest md5;
        if (param == null || param.length == 0){
            return null;
        }
        try {
            md5 = MessageDigest.getInstance(MD5);
            md5.update(param);
            return md5.digest();
        } catch (NoSuchAlgorithmException e) {
            System.err.println(e.getMessage());
        }
        return null;
    }

    /**
     *md5不可逆加密
     * @param secret
     * @return
     */
    public static String md5Encode(String secret){
        if (secret == null || "".equals(secret.trim())){
            return null;
        }
        byte[] retByte = new byte[0];
        try {
            retByte = MD5Encode(secret.getBytes("UTF-8"));
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        if (retByte != null){
            return bytesToHexString(retByte);
        }
        return null;
    }

    private static byte[] SHAEncode(byte[] param){
        MessageDigest sha;
        if (param == null || param.length == 0){
            return null;
        }
        try {
            sha = MessageDigest.getInstance(SHA);
            sha.update(param);
            return sha.digest();
        } catch (NoSuchAlgorithmException e) {
            System.err.println(e.getMessage());
        }
        return null;
    }

    /**
     * sha不可逆加密
     * @param secret
     * @return
     */
    public static String shaEncode(String secret){
        if (null == secret || "".equals(secret.trim())){
            return null;
        }

        byte[] retByte = new byte[0];
        try {
            retByte = SHAEncode(secret.getBytes("UTF-8"));
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        if (retByte != null) {
            return bytesToHexString(retByte);
        }

        return null;
    }

    private static byte[] AESEncode(byte[] param,String key){
        if (param == null || param.length == 0){
            return null;
        }
        try {
            KeyGenerator keygen = KeyGenerator.getInstance(AES);
            SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
            random.setSeed(key.getBytes(chart_set_utf8));
            keygen.init(128,random);
            SecretKey secretKey = keygen.generateKey();
            byte[] enCodeFormat = secretKey.getEncoded();
            SecretKeySpec keySpeck = new SecretKeySpec(enCodeFormat, AES);
            Cipher cipher = Cipher.getInstance(AES);
            cipher.init(Cipher.ENCRYPT_MODE,keySpeck);
            byte[] ret = cipher.doFinal(param);
            return ret;
        } catch (Exception e) {
            System.err.println(e.getMessage());
        }
        return null;
    }

    private static byte[] AESDecode(byte[] param,String key){
        if (param == null || param.length == 0){
            return null;
        }
        try {
            KeyGenerator keygen = KeyGenerator.getInstance(AES);
            SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
            random.setSeed(key.getBytes(chart_set_utf8));
            keygen.init(128,random);
            SecretKey secretKey = keygen.generateKey();
            byte[] enCodeFormat = secretKey.getEncoded();
            SecretKeySpec keySpeck = new SecretKeySpec(enCodeFormat, AES);
            Cipher cipher = Cipher.getInstance(AES);
            cipher.init(Cipher.DECRYPT_MODE,keySpeck);
            byte[] ret =  cipher.doFinal(param);
            return ret;
        } catch (Exception e) {
            System.err.println(e.getMessage());
        }
        return null;
    }

    /**
     *  可逆加密
     * @param secret
     * @param key
     * @return
     */
    public static String aesEncode(String secret,String key){
        if (secret == null || "".equals(secret.trim())
                || key == null || "".equals(key.trim())) {
            return null;
        }

        byte[] retByte = new byte[0];
        try {
            retByte = AESEncode(secret.getBytes(chart_set_utf8),key);
        } catch (UnsupportedEncodingException e) {
            System.err.println(e.getMessage());
        }
        if (retByte != null) {
            return bytesToHexString(retByte);
        }

        return null;
    }

    /**
     * 可逆解密
     * @param secret
     * @param key
     * @return
     */
    public static String aesDecode(String secret,String key){
        if (secret == null || "".equals(secret.trim())){
            return null;
        }
        byte[] encodeBytes = hexStringToBytes(secret);
        byte[] retByte = AESDecode(encodeBytes,key);
        if (retByte != null) {
            try {
                return new String(retByte,"UTF-8");
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }

        return null;
    }
}
