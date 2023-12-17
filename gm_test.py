#! /usr/bin/python
# encoding : utf-8
import time
import base64
from gmssl import sm2,sm4
import codecs
SM2_PRIVATE_KEY = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
SM2_PUBLIC_KEY = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
sm2_crypt = sm2.CryptSM2(public_key=SM2_PUBLIC_KEY, private_key=SM2_PRIVATE_KEY)

SM4_KEY = b'3l5butlj26hvv313'
SM4_IV = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' #  bytes类型
sm4_crypt = sm4.CryptSM4()

def base64_en(png_org,png_en):
    with open(png_org, 'rb') as f:
        image_base64 = str(base64.b64encode(f.read()), encoding='utf-8')
    with open(png_en,'wt') as f_en:
        f_en.write(image_base64)

def base64_de(png_en,png_de):
    with open(png_en,"r") as f:
        imgdata = base64.b64decode(f.read())
    with open(png_de,'wb+') as f_de:
        f_de.write(imgdata)

def sm2_en(png_org,png_en):
    with open(png_org, 'rb') as f:
        image_base64 = base64.b64encode(f.read())
        image_sm2 = str(sm2_crypt.encrypt(image_base64))
    with open(png_en,'wt') as f_en:
        f_en.write(image_sm2)

def sm2_de(png_en,png_de):
    with open(png_en,"r") as f:
        image_sm2 = codecs.escape_decode(bytes(f.read()[2:-1],encoding="utf-8"), "hex-escape")[0]
        image_base64 = sm2_crypt.decrypt(image_sm2)
        imgdata = base64.b64decode(image_base64)
    with open(png_de,'wb') as f_de:
        f_de.write(imgdata)

def sm4_en(png_org,png_en):
    sm4_crypt.set_key(SM4_KEY, sm4.SM4_ENCRYPT)
    time_start = time.time()
    print(time_start)
    with open(png_org, 'rb') as f:
        image_base64 = base64.b64encode(f.read())
        time_1 = time.time()
        print(time_1-time_start)
        image_sm4 = str(sm4_crypt.crypt_ecb(image_base64))
        time_2 = time.time()
        print(time_2 - time_1)
    with open(png_en,'wt') as f_en:
        f_en.write(image_sm4)

def sm4_de(png_en,png_de):
    sm4_crypt.set_key(SM4_KEY, sm4.SM4_DECRYPT)
    with open(png_en,"r") as f:
        image_sm4 = codecs.escape_decode(bytes(f.read()[2:-1],encoding="utf-8"), "hex-escape")[0]
        image_base64 = sm4_crypt.crypt_ecb(image_sm4)
        imgdata = base64.b64decode(image_base64)
    with open(png_de,'wb') as f_de:
        f_de.write(imgdata)


if __name__ == '__main__':
    #f_org ='bas.txt'
    #f_en ='basen.txt'
    #f_de ='basde.txt'
    # f_org = '1.png'
    # f_en = '12321.txt'
    # f_de = '123321.png'
    # pngfile_base64_en(p_org,p_en)
    # pngfile_base64_de(p_en,p_de)
    f_org = 'abc.pdf'
    f_en = '2.txt'
    f_de = 'asdf+z44.pdf'
    #sm2_en(f_org,f_en)
    #sm2_de(f_en,f_de)
    time_start = time.time()
    sm4_en(f_org,f_en)
    time_mid = time.time()
    print(time_mid-time_start)
    sm4_de(f_en,f_de)
    time_end = time.time()
    print(time_end-time_mid)