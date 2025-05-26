import os
import zlib
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

KEY = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
IV = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15'

def get_md5_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        # 파일을 chunk 단위로 읽어서 해시 계산
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def load_metadata():
    with open("encryption-metadata.json", "rt", encoding="utf-8") as f:
        metadata = json.load(f)
    
    return metadata

def decrypt(filename, blocks, original_size, key, iv):
    def check_decrypt_well(filename):
        basename = os.path.basename(filename)
        if basename.endswith(".enc"):
            basename = basename.replace(".enc", "")

        origin_file = f"D:\\ransomware_research\\실험\\ransomware\\govdocs_test\\{basename}"
        decrypt_md5 = get_md5_hash(filename)
        origin_md5 = get_md5_hash(origin_file)
        if decrypt_md5 == origin_md5:
            print("decrypt well!")
            os.rename(filename, f"D:\\ransomware_research\\실험\\ransomware\\govdocs_small\\{basename}")
        else:
            print("decrypt failed!")

    try:
        blocks.reverse()
        with open(filename, 'rb+') as f:
            for b in blocks:
                offset = b['offset']
                _size = b['size']
                ispadded = b['padd']
                f.seek(offset, 0)
                encrypted_bin = f.read(_size)
                aes = AES.new(key, AES.MODE_CBC, iv)
                dec_bin = aes.decrypt(encrypted_bin)
                if ispadded:
                    dec_bin = unpad(dec_bin, AES.block_size)
                f.seek(offset, 0)
                f.write(dec_bin)
            f.seek(0, 0)
            f.seek(original_size, 0)
            f.truncate()        
        check_decrypt_well(filename)            
    except Exception as e:
        print(e)

if __name__ == '__main__':
    metadatas = load_metadata()
    for metadata in metadatas:
        filename = metadata['filename']
        blocks = metadata['blocks']
        original_size = metadata['original_size']
        decrypt(filename, blocks, original_size, KEY, IV)
    pass