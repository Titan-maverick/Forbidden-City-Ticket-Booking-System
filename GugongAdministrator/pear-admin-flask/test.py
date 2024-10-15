from werkzeug.security import generate_password_hash

# 设置新的密码
new_password = "your_new_password"
# 生成哈希值
hashed_password = generate_password_hash(new_password)
print(hashed_password)
