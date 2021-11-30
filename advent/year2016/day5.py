import hashlib


def main():
    print(crack("ojvtpuvg"))


def crack(door_id):
    password = ""
    index = 0
    while len(password) < 8:
        hash_input = (door_id + str(index)).encode('utf-8')
        mhash = hashlib.md5(hash_input).hexdigest()
        # import pdb; pdb.set_trace()
        if mhash.startswith("00000"):
            print("hash=" + mhash)
            password += mhash[5]
            print("password=" + password)
        index += 1
    return password


if __name__ == "__main__":
    main()
