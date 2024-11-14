import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from bson import ObjectId

# Conectar a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["blog_database"]

# Colecciones
articles_collection = db["articles"]
users_collection = db["users"]
comments_collection = db["comments"]
tags_collection = db["tags"]
categories_collection = db["categories"]

class BlogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blog Manager")

        tk.Button(root, text="Manage Users", command=self.manage_users).grid(row=0, column=0)
        tk.Button(root, text="Manage Articles", command=self.manage_articles).grid(row=1, column=0)
        tk.Button(root, text="Manage Comments", command=self.manage_comments).grid(row=2, column=0)
        tk.Button(root, text="Manage Tags", command=self.manage_tags).grid(row=3, column=0)
        tk.Button(root, text="Manage Categories", command=self.manage_categories).grid(row=4, column=0)

    # CRUD para la colección de artículos con relación a tags y categorías
    def manage_articles(self):
        article_window = tk.Toplevel(self.root)
        article_window.title("Manage Articles")

        tk.Label(article_window, text="Title").grid(row=0, column=0)
        tk.Label(article_window, text="Date").grid(row=1, column=0)
        tk.Label(article_window, text="Text").grid(row=2, column=0)
        tk.Label(article_window, text="User ID").grid(row=3, column=0)
        tk.Label(article_window, text="Tag IDs (comma-separated)").grid(row=4, column=0)
        tk.Label(article_window, text="Category IDs (comma-separated)").grid(row=5, column=0)

        title_entry = tk.Entry(article_window)
        title_entry.grid(row=0, column=1)

        date_entry = tk.Entry(article_window)
        date_entry.grid(row=1, column=1)

        text_entry = tk.Entry(article_window)
        text_entry.grid(row=2, column=1)

        user_id_entry = tk.Entry(article_window)
        user_id_entry.grid(row=3, column=1)

        tags_entry = tk.Entry(article_window)
        tags_entry.grid(row=4, column=1)

        categories_entry = tk.Entry(article_window)
        categories_entry.grid(row=5, column=1)

        def add_article():
            title = title_entry.get()
            date = date_entry.get()
            text = text_entry.get()
            user_id = user_id_entry.get()
            tag_ids = [ObjectId(tag.strip()) for tag in tags_entry.get().split(",") if tag.strip()]
            category_ids = [ObjectId(category.strip()) for category in categories_entry.get().split(",") if category.strip()]

            if title and date and text and user_id:
                new_article = {
                    "title": title,
                    "date": date,
                    "text": text,
                    "user_id": ObjectId(user_id),
                    "tags": tag_ids,
                    "categories": category_ids
                }
                articles_collection.insert_one(new_article)
                messagebox.showinfo("Success", "Article added successfully!")
            else:
                messagebox.showwarning("Input error", "Title, Date, Text and User ID are required.")

        def delete_article():
            article_id = title_entry.get()
            if article_id:
                try:
                    article_obj_id = ObjectId(article_id)
                    # Verificar si el artículo existe
                    article = articles_collection.find_one({"_id": article_obj_id})
                    if article:
                        articles_collection.delete_one({"_id": article_obj_id})
                        messagebox.showinfo("Success", "Article deleted successfully!")
                    else:
                        messagebox.showwarning("Not found", "Article not found.")
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid ID format: {e}")
            else:
                messagebox.showwarning("Input error", "Article ID is required.")


        def update_article():
            article_id = title_entry.get()
            date = date_entry.get()
            text = text_entry.get()
            user_id = user_id_entry.get()
            tag_ids = [ObjectId(tag.strip()) for tag in tags_entry.get().split(",") if tag.strip()]
            category_ids = [ObjectId(category.strip()) for category in categories_entry.get().split(",") if category.strip()]

            if article_id:
                article_obj_id = ObjectId(article_id)
                articles_collection.update_one(
                    {"_id": article_obj_id},
                    {"$set": {"date": date, "text": text, "user_id": ObjectId(user_id), "tags": tag_ids, "categories": category_ids}}
                )
                messagebox.showinfo("Success", "Article updated successfully!")
            else:
                messagebox.showwarning("Input error", "Article ID are required.")
        
        def read_articles():
            articles = articles_collection.find()
            article_list = "\n".join([f"{article['title']} - {article['date']}" for article in articles])
            messagebox.showinfo("Articles", article_list if article_list else "No articles found.")


        add_button = tk.Button(article_window, text="Add Article", command=add_article)
        add_button.grid(row=7, column=0)

        delete_button = tk.Button(article_window, text="Delete Article", command=delete_article)
        delete_button.grid(row=7, column=1)

        update_button = tk.Button(article_window, text="Update Article", command=update_article)
        update_button.grid(row=7, column=2)

        read_button = tk.Button(article_window, text="Read Articles", command=read_articles)
        read_button.grid(row=7, column=3)


    # CRUD para la colección de usuarios
    def manage_users(self):
        user_window = tk.Toplevel(self.root)
        user_window.title("Manage Users")

        tk.Label(user_window, text="Username").grid(row=0, column=0)
        tk.Label(user_window, text="Email").grid(row=1, column=0)

        username_entry = tk.Entry(user_window)
        username_entry.grid(row=0, column=1)

        email_entry = tk.Entry(user_window)
        email_entry.grid(row=1, column=1)

        def add_user():
            username = username_entry.get()
            email = email_entry.get()
            if username and email:
                new_user = {"username": username, "email": email}
                users_collection.insert_one(new_user)
                messagebox.showinfo("Success", "User added successfully!")
            else:
                messagebox.showwarning("Input error", "Both Username and Email are required.")

        def delete_user():
            user_id = username_entry.get()
            if user_id:
                try:
                    user_obj_id = ObjectId(user_id)
                    # Verificar si el usuario existe
                    user = users_collection.find_one({"_id": user_obj_id})
                    if user:
                        users_collection.delete_one({"_id": user_obj_id})
                        messagebox.showinfo("Success", "User deleted successfully!")
                    else:
                        messagebox.showwarning("Not found", "User not found.")
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid ID format: {e}")
            else:
                messagebox.showwarning("Input error", "User ID is required.")

        def update_user():
            user_id = username_entry.get()
            email = email_entry.get()

            if user_id and email:
                user_obj_id = ObjectId(user_id)
                users_collection.update_one(
                    {"_id": user_obj_id},
                    {"$set": {"email": email}}
                )
                messagebox.showinfo("Success", "User updated successfully!")
            else:
                messagebox.showwarning("Input error", "User ID is required.")

        def read_users():
            users = users_collection.find()
            user_list = "\n".join([f"{user['username']} - {user['email']}" for user in users])
            messagebox.showinfo("Users", user_list if user_list else "No users found.")

        add_button = tk.Button(user_window, text="Add User", command=add_user)
        add_button.grid(row=3, column=0)

        delete_button = tk.Button(user_window, text="Delete User", command=delete_user)
        delete_button.grid(row=3, column=1)

        update_button = tk.Button(user_window, text="Update User", command=update_user)
        update_button.grid(row=3, column=2)

        update_button = tk.Button(user_window, text="Read Users", command=read_users)
        update_button.grid(row=3, column=3)

    # CRUD para la colección de comentarios
    def manage_comments(self):
        comment_window = tk.Toplevel(self.root)
        comment_window.title("Manage Comments")

        tk.Label(comment_window, text="Article ID").grid(row=0, column=0)
        tk.Label(comment_window, text="User ID").grid(row=1, column=0)
        tk.Label(comment_window, text="Name").grid(row=2, column=0)
        tk.Label(comment_window, text="Comment Text").grid(row=3, column=0)

        article_id_entry = tk.Entry(comment_window)
        article_id_entry.grid(row=0, column=1)

        user_id_entry = tk.Entry(comment_window)
        user_id_entry.grid(row=1, column=1)

        name_entry = tk.Entry(comment_window)
        name_entry.grid(row=2, column=1)

        text_entry = tk.Entry(comment_window)
        text_entry.grid(row=3, column=1)

        def add_comment():
            article_id = article_id_entry.get()
            user_id = user_id_entry.get()
            name = name_entry.get()
            text = text_entry.get()
            if article_id and user_id and name and text:
                new_comment = {
                    "article_id": ObjectId(article_id),
                    "user_id": ObjectId(user_id),
                    "name": name,
                    "text": text
                }
                comments_collection.insert_one(new_comment)
                messagebox.showinfo("Success", "Comment added successfully!")
            else:
                messagebox.showwarning("Input error", "Article ID, User ID, Name and Text are required.")

        def delete_comment():
            comment_id = text_entry.get()
            if comment_id:
                try:
                    comment_obj_id = ObjectId(comment_id)
                    # Verificar si el comentario existe
                    comment = comments_collection.find_one({"_id": comment_obj_id})
                    if comment:
                        comments_collection.delete_one({"_id": comment_obj_id})
                        messagebox.showinfo("Success", "Comment deleted successfully!")
                    else:
                        messagebox.showwarning("Not found", "Comment not found.")
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid ID format: {e}")
            else:
                messagebox.showwarning("Input error", "Comment ID is required.")

        def update_comment():
            comment_id = name_entry.get()
            text = text_entry.get()
            article_id = article_id_entry.get()
            user_id = user_id_entry.get()

            if comment_id:
                comment_obj_id = ObjectId(comment_id)
                comments_collection.update_one(
                    {"_id": comment_obj_id},
                    {"$set": {"text": text, "article_id": ObjectId(article_id), "user_id": ObjectId(user_id)}}
                )
                messagebox.showinfo("Success", "Comment updated successfully!")
            else:
                messagebox.showwarning("Input error", "Comment ID is required.")

        def read_comments():
            comments = comments_collection.find()
            comment_list = "\n".join([f"{comment['text']} - {comment['user_id']}" for comment in comments])
            messagebox.showinfo("Comments", comment_list if comment_list else "No comments found.")


        add_button = tk.Button(comment_window, text="Add Comment", command=add_comment)
        add_button.grid(row=4, column=0)

        delete_button = tk.Button(comment_window, text="Delete Comment", command=delete_comment)
        delete_button.grid(row=4, column=1)

        update_button = tk.Button(comment_window, text="Update Comment", command=update_comment)
        update_button.grid(row=4, column=2)

        read_button = tk.Button(comment_window, text="Read Comments", command=read_comments)
        read_button.grid(row=4, column=3) 


    # CRUD para la colección de tags
    def manage_tags(self):
        tag_window = tk.Toplevel(self.root)
        tag_window.title("Manage Tags")

        tk.Label(tag_window, text="Name").grid(row=0, column=0)
        tk.Label(tag_window, text="URL").grid(row=1, column=0)
        tk.Label(tag_window, text="Article IDs (comma-separated)").grid(row=2, column=0)

        name_entry = tk.Entry(tag_window)
        name_entry.grid(row=0, column=1)

        url_entry = tk.Entry(tag_window)
        url_entry.grid(row=1, column=1)

        articles_entry = tk.Entry(tag_window)
        articles_entry.grid(row=2, column=1)

        def add_tag():
            name = name_entry.get()
            url = url_entry.get()
            article_ids = [ObjectId(article.strip()) for article in articles_entry.get().split(",") if article.strip()]
            if name and url:
                new_tag = {"name": name, "url": url, "articles": article_ids}
                tags_collection.insert_one(new_tag)
                messagebox.showinfo("Success", "Tag added successfully!")
            else:
                messagebox.showwarning("Input error", "Name and url are required.")

        def delete_tag():
            tag_id = name_entry.get()
            if tag_id:
                try:
                    tag_obj_id = ObjectId(tag_id)
                    # Verificar si el tag existe
                    tag = tags_collection.find_one({"_id": tag_obj_id})
                    if tag:
                        tags_collection.delete_one({"_id": tag_obj_id})
                        messagebox.showinfo("Success", "Tag deleted successfully!")
                    else:
                        messagebox.showwarning("Not found", "Tag not found.")
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid ID format: {e}")
            else:
                messagebox.showwarning("Input error", "Tag ID is required.")


        def update_tag():
            tag_id = name_entry.get()
            url = url_entry.get()
            article_ids = [ObjectId(article.strip()) for article in articles_entry.get().split(",") if article.strip()]

            if tag_id:
                tag_obj_id = ObjectId(tag_id)
                tags_collection.update_one(
                    {"_id": tag_obj_id},
                    {"$set": {"url": url, "articles": article_ids}}
                )
                messagebox.showinfo("Success", "Tag updated successfully!")
            else:
                messagebox.showwarning("Input error", "Tag ID is required.")
        
        def read_tags():
            tags = tags_collection.find()
            tag_list = "\n".join([f"{tag['_id']} - {tag['name']}" for tag in tags])
            messagebox.showinfo("Tags", tag_list if tag_list else "No tags found.")

        add_button = tk.Button(tag_window, text="Add Tag", command=add_tag)
        add_button.grid(row=3, column=0)

        delete_button = tk.Button(tag_window, text="Delete Tag", command=delete_tag)
        delete_button.grid(row=3, column=1)

        update_button = tk.Button(tag_window, text="Update Tag", command=update_tag)
        update_button.grid(row=3, column=2)

        read_button = tk.Button(tag_window, text="Read Tags", command=read_tags)
        read_button.grid(row=3, column=3)


    # CRUD para la colección de categorías
    def manage_categories(self):
        category_window = tk.Toplevel(self.root)
        category_window.title("Manage Categories")

        tk.Label(category_window, text="Name").grid(row=0, column=0)
        tk.Label(category_window, text="URL").grid(row=1, column=0)
        tk.Label(category_window, text="Article IDs (comma-separated)").grid(row=2, column=0)

        name_entry = tk.Entry(category_window)
        name_entry.grid(row=0, column=1)

        url_entry = tk.Entry(category_window)
        url_entry.grid(row=1, column=1)

        articles_entry = tk.Entry(category_window)
        articles_entry.grid(row=2, column=1)

        def add_category():
            name = name_entry.get()
            url = url_entry.get()
            article_ids = [ObjectId(article.strip()) for article in articles_entry.get().split(",") if article.strip()]
            if name and url:
                new_category = {"name": name, "url": url, "articles": article_ids}
                categories_collection.insert_one(new_category)
                messagebox.showinfo("Success", "Category added successfully!")
            else:
                messagebox.showwarning("Input error", "All fields are required.")

        def delete_category():
            category_id = name_entry.get()  # Cambia name_entry si usas otro campo para ingresar el ID de la categoría
            if category_id:
                try:
                    category_obj_id = ObjectId(category_id)
                    # Verificar si la categoría existe
                    category = categories_collection.find_one({"_id": category_obj_id})
                    if category:
                        categories_collection.delete_one({"_id": category_obj_id})
                        messagebox.showinfo("Success", "Category deleted successfully!")
                    else:
                        messagebox.showwarning("Not found", "Category not found.")
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid ID format: {e}")
            else:
                messagebox.showwarning("Input error", "Category ID is required.")


        def update_category():
            category_id = name_entry.get()
            url = url_entry.get()
            article_ids = [ObjectId(article.strip()) for article in articles_entry.get().split(",") if article.strip()]

            if category_id:
                category_obj_id = ObjectId(category_id)
                categories_collection.update_one(
                    {"_id": category_obj_id},
                    {"$set": {"url": url, "articles": article_ids}}
                )
                messagebox.showinfo("Success", "Category updated successfully!")
            else:
                messagebox.showwarning("Input error", "Category ID is required.")
        
        def read_categories():
            categories = categories_collection.find()
            category_list = "\n".join([f"{category['_id']} - {category['name']}" for category in categories])
            messagebox.showinfo("Categories", category_list if category_list else "No categories found.")


        add_button = tk.Button(category_window, text="Add Category", command=add_category)
        add_button.grid(row=3, column=0)

        delete_button = tk.Button(category_window, text="Delete Category", command=delete_category)
        delete_button.grid(row=3, column=1)

        add_button = tk.Button(category_window, text="Update Category", command=update_category)
        add_button.grid(row=3, column=2)

        read_button = tk.Button(category_window, text="Read Categories", command=read_categories)
        read_button.grid(row=3, column=3) 


if __name__ == "__main__":
    root = tk.Tk()
    app = BlogApp(root)
    root.mainloop()
