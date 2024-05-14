import multiprocessing

def worker(data, q):
    q.put(data * 2)

if __name__ == "__main__":
    # 创建一个共享的队列
    manager = multiprocessing.Manager()
    queue = manager.Queue()

    # 准备要处理的数据
    data = [1, 2, 3, 4, 5]

    # 创建进程池
    pool = multiprocessing.Pool()

    # 使用map_async方法启动多个进程，将共享的队列作为额外参数传递给worker函数
    pool.map_async(worker, data, initializer=lambda: None, initargs=(queue,))

    # 关闭进程池
    pool.close()
    pool.join()

    # 打印队列中的结果
    while not queue.empty():
        print(queue.get())
