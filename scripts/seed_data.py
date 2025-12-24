"""
RUN: python3 manage.py shell < scripts/seed_data.py
"""

from django.contrib.auth.models import User
from articles.models import Article, Comment
from tags.models import Tag
from django.utils.text import slugify

# User.objects.all().delete()
# Article.objects.all().delete()
# Tag.objects.all().delete()
# Comment.objects.all().delete()

print("=== Creating test data ===\n")

print("1. Creating Users...")
user1, _ = User.objects.get_or_create(
    username='john_doe',
    defaults={
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Doe'
    }
)
user1.set_password('password123')
user1.save()
print(f"   ✓ Created user: {user1.username}")

user2, _ = User.objects.get_or_create(
    username='jane_smith',
    defaults={
        'email': 'jane@example.com',
        'first_name': 'Jane',
        'last_name': 'Smith'
    }
)
user2.set_password('password123')
user2.save()
print(f"   ✓ Created user: {user2.username}")

user3, _ = User.objects.get_or_create(
    username='admin_user',
    defaults={
        'email': 'admin@example.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True
    }
)
user3.set_password('admin123')
user3.save()
print(f"   ✓ Created user: {user3.username}\n")

# 2. Create Tags
print("2. Creating Tags...")
tags_data = ['Python', 'Django', 'REST API', 'Web Development', 'Database']
tags = []
for tag_name in tags_data:
    tag, _ = Tag.objects.get_or_create(
        name=tag_name,
        defaults={'slug': slugify(tag_name)}
    )
    tags.append(tag)
    print(f"   ✓ Created tag: {tag.name}")
print()

# 3. Create Articles
print("3. Creating Articles...")
articles_data = [
    {
        'title': 'Getting Started with Django REST Framework',
        'content': 'Django REST Framework (DRF) is a powerful framework for building REST APIs in Django. It provides tools like serializers, viewsets, routers, and permissions to help you build APIs quickly and efficiently.',
        'author': user1,
        'tags': [tags[1], tags[2], tags[3]]  # Django, REST API, Web Development
    },
    {
        'title': 'Python Best Practices',
        'content': 'In this article, we will explore the best practices for writing Python code. From using virtual environments, writing clean code, to optimization techniques.',
        'author': user2,
        'tags': [tags[0], tags[3]]  # Python, Web Development
    },
    {
        'title': 'Database Design Patterns',
        'content': 'Good database design is the foundation of any successful web application. This article will introduce common design patterns and how to apply them to your projects.',
        'author': user1,
        'tags': [tags[4], tags[1]]  # Database, Django
    },
    {
        'title': 'Permissions and Authentication in DRF',
        'content': 'Security is a crucial aspect of any web application. Django REST Framework provides built-in permissions and authentication classes to help protect your API.',
        'author': user2,
        'tags': [tags[1], tags[2]]  # Django, REST API
    },
    {
        'title': 'Advanced Django ORM Queries',
        'content': 'Django ORM is a powerful tool for interacting with databases. This article will explore advanced queries like Q objects, aggregations, annotations and much more.',
        'author': user1,
        'tags': [tags[1], tags[4]]  # Django, Database
    }
]

articles = []
for article_data in articles_data:
    article, created = Article.objects.get_or_create(
        title=article_data['title'],
        defaults={
            'slug': slugify(article_data['title']),
            'content': article_data['content'],
            'author': article_data['author']
        }
    )
    # Add tags
    article.tags.set(article_data['tags'])
    articles.append(article)
    status = "✓ Created" if created else "→ Already exists"
    print(f"   {status}: {article.title}")
print()

# 4. Create Comments
print("4. Creating Comments...")
comments_data = [
    {'article': articles[0], 'author': user2, 'content': 'Great article! Thanks for sharing.'},
    {'article': articles[0], 'author': user3, 'content': 'Can you explain more about serializers?'},
    {'article': articles[1], 'author': user1, 'content': 'I completely agree with these best practices.'},
    {'article': articles[2], 'author': user2, 'content': 'The N+1 query problem is a common issue.'},
    {'article': articles[3], 'author': user1, 'content': 'Can you provide a more specific example?'},
]

for idx, comment_data in enumerate(comments_data):
    comment, created = Comment.objects.get_or_create(
        article=comment_data['article'],
        author=comment_data['author'],
        defaults={
            'content': comment_data['content'],
            'slug': slugify(comment_data['content'][:50] + str(idx))
        }
    )
    status = "✓ Created" if created else "→ Already exists"
    print(f"   {status}: Comment on '{comment_data['article'].title}' by {comment_data['author'].username}")
print()

# 5. Add favorites
print("5. Adding Favorites...")
articles[0].favorited_by.add(user2, user3)
articles[1].favorited_by.add(user1, user3)
articles[2].favorited_by.add(user1)
articles[3].favorited_by.add(user2)
articles[4].favorited_by.add(user1, user2, user3)
print(f"   ✓ Added favorites\n")

print("=== ✅ Test data created successfully! ===\n")

# Print summary information
print("📊 Summary Information:")
print(f"   Users: {User.objects.count()}")
print(f"   Articles: {Article.objects.count()}")
print(f"   Comments: {Comment.objects.count()}")
print(f"   Tags: {Tag.objects.count()}")
print("\n🔑 Login Information:")
print(f"   Username: john_doe, Password: password123")
print(f"   Username: jane_smith, Password: password123")
print(f"   Username: admin_user, Password: admin123")
