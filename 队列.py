import queue

# 创建基本队列
# queue.Queue(maxsize=0)创建一个队列对象（队列容量），若maxsize小于或者等于0，队列大小没有限制
Q = queue.Queue()
print(Q)


# 1.基本方法
print(Q.queue)  # 查看队列中所有元素
print(Q.qsize())  # 返回队列的大小
print(Q.empty())  # 判断队空
print(Q.full())  # 判断队满

# 2.获取队列，0--5
# Queue.put（item，block = True，timeout = None ）将对象放入队列，阻塞调用（block=False抛异常），无等待时间
for i in range(5):
    print(Q.queue)
# Queue.put_nowait(item)相当于 put(item, False).


# 3.读队列，0--5
# Queue.get(block=True, timeout=None)读出队列的一个元素，阻塞调用，无等待时间
while not Q.empty():
    print(Q.get())
# Queue.get_nowait()相当于get(False).取数据，如果没数据抛queue.Empty异常


# 4.另两种涉及等待排队任务的方法
# Queue.task_done()在完成一项工作后，向任务已经完成的队列发送一个信号
# Queue.join()阻止直到队列中的所有项目都被获取并处理。即等到队列为空再执行别的操作
a = {"code":20000,"et":{"OrderId":"14999087723627520","Gold":8000,"NGold":61000,"Type":3,"Data":{"Residue":95,"FreeGold":8000,"BonusGold":6000,"Gold":8000,"Rpoints":[{"AwardLins":{"3":4},"Gold":4000,"isFree":false,"Points":[5,7,4,7,9,14,3,9,6,8,8,2,3,3,7],"AdPoints":{"3":[5,6,12,13]},"Plan":1,"Residue":0,"LinePoints":{"3":[[5,6,12,13]]},"ApiPoints":null,"MAXAwIndex":3,"MAXAwComProbability":40,"FreeGold":0,"BonusGold":0,"Type":0},{"AwardLins":{"5":3},"Gold":4000,"isFree":false,"Points":[5,5,5,4,9,5,7,4,7,8,8,2,9,6,7],"AdPoints":{"5":[0,5,1,2]},"Plan":2,"Residue":0,"LinePoints":{"5":[[0,1,2],[5,1,2]]},"ApiPoints":null,"MAXAwIndex":5,"MAXAwComProbability":10,"FreeGold":0,"BonusGold":0,"Type":0},{"AwardLins":{},"Gold":0,"isFree":False,"Points":[12,6,8,4,9,12,7,4,7,8,8,2,9,6,7],"AdPoints":{},"Plan":0,"Residue":0,"LinePoints":{},"ApiPoints":null,"MAXAwIndex":0,"MAXAwComProbability":0,"FreeGold":0,"BonusGold":0,"Type":0}],"Type":3}},"ms":null,"newID":null}