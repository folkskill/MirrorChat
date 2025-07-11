import mysql.connector

class SQLLoader():
    def __init__(self, host='localhost', user='your_username', password='your_password', database='your_database', port=3306):
        # 建立 MySQL 数据库连接
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port  # 新增端口参数
            )
            # 创建一个游标对象，用于执行 SQL 语句
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"连接数据库时出错: {err}")
            self.conn = None  # 连接失败时将 conn 设为 None

    def create_table(self):
        """创建存储版本信息的表"""
        if self.conn and self.conn.is_connected():
            create_table_query = """
            CREATE TABLE IF NOT EXISTS version_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                version VARCHAR(255) NOT NULL
            )
            """
            try:
                self.cursor.execute(create_table_query)
                self.conn.commit()
            except mysql.connector.Error as err:
                print(f"创建表时出错: {err}")

    def insert_version(self, version):
        """插入版本信息到表中"""
        if self.conn and self.conn.is_connected():
            insert_query = "INSERT INTO version_info (version) VALUES (%s)"
            try:
                self.cursor.execute(insert_query, (version,))
                self.conn.commit()
                print(f"成功插入版本信息: {version}")
            except mysql.connector.Error as err:
                print(f"插入数据时出错: {err}")

    def get_version(self):
        """从数据库中查询并返回最新版本字符串"""
        if self.conn and self.conn.is_connected():
            select_query = "SELECT version FROM version_info ORDER BY id DESC LIMIT 1"
            try:
                self.cursor.execute(select_query)
                result = self.cursor.fetchone()
                if result:
                    return result[0]
                else:
                    print("数据库中没有版本信息。")
            except mysql.connector.Error as err:
                print(f"查询版本信息时出错: {err}")
        return None

    def is_latest_version(self, version):
        """判断传入的版本号是否为最新版本"""
        latest_version = self.get_version()
        if latest_version is None:
            return False
        return version == latest_version

    def close_connection(self):
        # 关闭数据库连接
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

def createCloudCounfigsql() -> SQLLoader:
    return SQLLoader(
        host='mysql2.sqlpub.com', 
        user='mirroradmin', 
        password='cZGus9c0TrfhaLyd', 
        database='mirrorchat_data',
        port=3307  # 单独指定端口号
    )

def checkDataInStarted() -> dict:
    current_version = open("VERSION.txt",'r').read()
    sqlL = createCloudCounfigsql()
    if sqlL.conn and sqlL.conn.is_connected():
        # 查询并打印版本信息
        version = sqlL.get_version()
        # 判断是否为最新版本
        is_latest = sqlL.is_latest_version(current_version)
        sqlL.close_connection()

        return {
            "current_version": current_version,
            "version": version,
            "is_latest": is_latest,
        }
    else:
        sqlL.close_connection()
        return None