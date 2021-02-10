import time
import threading
import random
import queue

num_reader = 4
num_writer = 6
write_action = 10

BufferLock = threading.Lock() 
Buffer_size = 5
Buffer = [queue.Queue(Buffer_size),  write_action * num_writer]

class ReadThread(threading.Thread):
    # new Thread
  def __init__(self, threadID, name):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name

  def run(self):
    while True:
      
      # Get lock to synchronize threads
      BufferLock.acquire()
      if Buffer[1] <= 0:
        BufferLock.release()
        break
      
      if not Buffer[0].empty():
        print("Reader " + str(self.name) + " : " + Buffer[0].get())
        Buffer[1] -= 1

      BufferLock.release()

      time.sleep(random.randint(1,5))


class WriteThread(threading.Thread):
    # new Thread
  def __init__(self, threadID, name, num_action):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.action = num_action

  def run(self):
    while self.action:
      
      # Get lock to synchronize threads
      BufferLock.acquire()
      if not Buffer[0].full():
        c = chr(97 + random.randint(0,25))
        print("Writer " + str(self.name) + " : " + c)
        Buffer[0].put(c)
        self.action -= 1
      BufferLock.release()
      time.sleep(random.randint(1,5))

# main
if __name__ == "__main__":
  print("Start buffer")
  
  read_threads = []
  write_threads = []

  # Create new threads
  for i in range(num_reader):
    thread = ReadThread(i, "RThread" + str(i))
    read_threads.append(thread)
    thread.start()

  for i in range(num_writer):
    thread = WriteThread(i, "WThread" + str(i), write_action)
    write_threads.append(thread)
    thread.start()


  # Wait for all threads to complete
  for t in read_threads:
    t.join()

  print("all threads finish")
  