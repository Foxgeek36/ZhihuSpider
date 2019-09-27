# 原始API，这部分不允许修改

- [获得某个问题的所有回答](https://www.zhihu.com/api/v4/questions/319783573/answers?include=data[*].is_normal,content,voteup_count,created_time;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&offset=&limit=3&sort_by=default&platform=desktop)

- [获得answer id 指定的回答](https://www.zhihu.com/api/v4/answers/475819518?include=data[*].voteup_count,content)

- [获得作者公开的个人信息](https://www.zhihu.com/api/v4/members/xie-qian-qian-20-2?include=allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics')

- [获得作者公开的个人信息(简要)](https://www.zhihu.com/api/v4/members/xie-qian-qian-20-2?include=allow_message)

- [获得某个用户被收录的回答](https://www.zhihu.com/api/v4/members/xie-qian-qian-20-2/marked-answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,collapsed_by,suggest_edit,comment_count,can_comment,content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question,excerpt,is_labeled,label_info,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,is_recognized;data[*].author.badge[?(type=best_answerer)].topics&offset=0&limit=20&sort_by=created)

- [获得某个用户按点赞数排序的回答](https://www.zhihu.com/api/v4/members/xie-qian-qian-20-2/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,collapsed_by,suggest_edit,comment_count,can_comment,content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question,excerpt,is_labeled,label_info,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,is_recognized;data[*].author.badge[?(type=best_answerer)].topics&offset=0&limit=20&sort_by=voteups)

- [获得某个用户按时间排序的回答](https://www.zhihu.com/api/v4/members/xie-qian-qian-20-2/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,collapsed_by,suggest_edit,comment_count,can_comment,content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question,excerpt,is_labeled,label_info,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp,is_recognized;data[*].author.badge[?(type=best_answerer)].topics&offset=0&limit=20&sort_by=created)

- [获得某个用户提出的问题](https://www.zhihu.com/api/v4/members/xie-qian-qian-20-2/questions?include=data[*].created,answer_count,follower_count,author,admin_closed_comment&offset=0&limit=20)

- [获得某个用户的想法](https://www.zhihu.com/api/v4/members/xie-qian-qian-20-2/pins?offset=0&limit=20&includes=data[*].upvoted_followees,admin_closed_comment)

- [获得某个用户的专栏](https://www.zhihu.com/api/v4/members/xie-qian-qian-20-2/column-contributions?include=data[*].column.intro,followers,articles_count&offset=0&limit=20)

- [获得有关专栏的信息](https://www.zhihu.com/api/v4/columns/learning-to-learn?include=title,intro,description,image_url,articles_count,followers,is_following,last_article.created)

- [获得专栏下的文章信息](https://zhuanlan.zhihu.com/api/columns/learning-to-learn/articles?include=data[*].admin_closed_comment,comment_count,suggest_edit,is_title_image_full_screen,can_comment,upvoted_followees,can_open_tipjar,can_tip,voteup_count,voting,topics,review_info,author.is_following,is_labeled,label_info)

- [某个用户按时间排序的文章](https://www.zhihu.com/api/v4/members/xie-qian-qian-20-2/articles?include=data[*].comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,can_comment,comment_permission,admin_closed_comment,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info;data[*].author.badge[?(type=best_answerer)].topics&offset=0&limit=20&sort_by=created)

- [某个用户按点赞数排序的文章](https://www.zhihu.com/api/v4/members/xie-qian-qian-20-2/articles?include=data[*].comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,can_comment,comment_permission,admin_closed_comment,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info;data[*].author.badge[?(type=best_answerer)].topics&offset=0&limit=20&sort_by=voteups)

- [话题-精华](https://www.zhihu.com/api/v4/topics/19559450/feeds/essence?include=data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;&limit=10)