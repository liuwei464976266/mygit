# 导入jpype模块
import jpype
import os

if __name__ == "__main__":
    # python要调用的java的jar包路径
    jarpath = os.path.join(os.path.abspath("."), "D:\code\helloword.jar")

    # 获取jvm.dll的文件路径
    jvmPath = jpype.getDefaultJVMPath()

    # 使用jpype开启虚拟机
    jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % jarpath)

    # ②、加载java类（参数是java的长类名）
    javaClass = jpype.JClass("com.liuwei.app.variable")

    # 实例化java对象
    # javaInstance = javaClass()

    # ③、调用java方法，由于我写的是静态方法，直接使用类名就可以调用方法
    javaClass.show()