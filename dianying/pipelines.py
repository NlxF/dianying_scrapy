#coding:utf-8
from nanjing.models import Nanjing, Director, AllActors, AllType, AllZone, Links


class DianyingPipeline(object):
    def process_item(self, item, spider):
        pics = []
        #导演(主导演)
        director = Director.objects.get_or_create(name=item['director'][0])
        #主演列表
        starrings = [AllActors.objects.get_or_create(name=name) for name in item['starring']]
         #类型列表
        types = [AllType.objects.get_or_create(type=t) for t in item['type']]
        #地区(主要地区)
        zones = AllZone.objects.get_or_create(zone=item['zone'][0])
        for pic in item['images'][1:]:
            pics.append(pic.get('path', ''))
        movie = Nanjing(
            title=item['title'][0].strip(),
            director=director[0],
            zone=zones[0],
            image_upload=','.join(pics),
            image_search=item['images'][0].get('path', ''),
            showtime='/'.join(item['showtime']),
            movie_time=item['movie_long'][0],
            score1=float(item['score1'][0]),
            score2=float(item['score2'][0]),
            summary=item['story'][0]
        )
        #一个movie创建完成
        movie.save()
        #正向保存m2m关系
        for s, b in starrings:
            movie.starring.add(s)
        for t, b in types:
            movie.tags.add(t)

        #下载链接和资源大小
        downloads = [
            Links.objects.create(link=l, size=s, nanjing=movie) for l, s in zip(item['download'], item['size'])
        ]
        #保存Foreign外键关系
        # director[0].directors.add(movie)
        # director[0].save()
        # zones[0].movie_zone.add(movie)
        # zones[0].save()
        #反向保存m2m关系
        for s, b in starrings:
            s.actors.add(movie)
        for t, b in types:
            t.movie_tags.add(movie)
        for d in downloads:
            movie.download.add(d)
        return item
