import time


def demo():
    print(">>> Start")
    for i in range(789):
        if i % 10 == 0:
            time.sleep(0.2)
            print("\r进度： {:.2f}%".format(100 * i / 788), end='')
    print("\r进度： 100.00%")
    print('>>> Done!')


if __name__ == '__main__':
    demo()