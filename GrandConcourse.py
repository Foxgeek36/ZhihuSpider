warehouse = r"C:\Users\Milloy\Desktop"
make_as_book = True
answer_id = ''  # v
column_id = ''  # v
article_id = ''  # v
question_id = '318163620'  # v
topic_id = ''  # v
user_id_for_answers = ''  # v
user_id_for_articles = ''  # v
collection_id = ''

if user_id_for_answers != '':
    from zhihu.user import user_answers

    user_answers(user_id_for_answers, warehouse)
if user_id_for_articles != '':
    from zhihu.user import user_articles

    user_articles(user_id_for_articles, warehouse)
if column_id != '':
    from zhihu.article import articles

    articles(column_id, warehouse)
if article_id != '':
    from zhihu.article import article

    a = article(article_id, warehouse)
    print(a)
if question_id != '':
    if not make_as_book:
        from zhihu.question import answers

        a = answers(question_id, warehouse)

    else:
        from zhihu.question import make_answers_as_book

        a = make_answers_as_book(question_id, warehouse)
if answer_id != '':
    from zhihu.question import answer

    a = answer(answer_id, warehouse)
    print(a)
if topic_id != '':
    from zhihu.topic import topic_essence

    topic_essence(topic_id, warehouse)

if collection_id != '':
    from zhihu.collection import collection

    collection(collection_id, warehouse)

# 说明：
# 这是脚本的启动入口，将目标id填入相应的位置，并把不需要的目标id设
# 为空（''）点击运行即可启动运行脚本。脚本通过检测相应id是否为空，
# 从而选择运行对应的模块，所以不需要的目标id一定要设置为空。


