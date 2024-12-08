class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be a string between 5 and 50 characters.")
        if not isinstance(author, Author):
            raise ValueError("Author must be an instance of the Author class.")
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")

        self._title = title
        self._author = author
        self._magazine = magazine
        Article.all.append(self)

        # Automatically add the article to the author and magazine
        author._articles.append(self)
        magazine.add_article(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        raise AttributeError("Cannot change article title once set.")

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise ValueError("Author must be an instance of the Author class.")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        self._magazine = value


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot change author name once set.")

    def add_article(self, magazine, title):
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        if not isinstance(title, str) or len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be a string between 5 and 50 characters.")
        article = Article(self, magazine, title)
        return article

    def articles(self):
        return self._articles

    def magazines(self):
        mags = list(set(article.magazine for article in self._articles))
        return mags if mags else None

    def topic_areas(self):
        areas = list({magazine.category for magazine in self.magazines() or []})
        return areas if areas else None


class Magazine:
    all = []

    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._name = name
        self._category = category
        self._articles = []
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = value

    def add_article(self, article):
        if not isinstance(article, Article):
            raise ValueError("Only Article instances can be added.")
        self._articles.append(article)

    def articles(self):
        return self._articles or None

    def contributors(self):
        contributors = list(set(article.author for article in self._articles))
        return contributors if contributors else None

    def article_titles(self):
        titles = [article.title for article in self._articles]
        return titles if titles else None

    def contributing_authors(self):
        author_counts = {}
        for article in self._articles:
            author = article.author
            author_counts[author] = author_counts.get(author, 0) + 1
        authors = [author for author, count in author_counts.items() if count > 2]
        return authors if authors else None

    @staticmethod
    def top_publisher():
        if not Magazine.all:
            return None  # No magazines exist

        # Find the magazine(s) with the most articles
        max_articles = 0
        top_magazine = None

        for magazine in Magazine.all:
            article_count = len(magazine.articles() or [])
            if article_count > max_articles:
                max_articles = article_count
                top_magazine = magazine

        return top_magazine