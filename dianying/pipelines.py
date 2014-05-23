#coding:utf-8
from nanjing.models import Nanjing, Director, AllActors, AllType, AllZone, Links


class DianyingPipeline(object):

    def process_item(self, item, spider):
        pics = []
        director = Director.objects.get_or_create(name=item['director'][0])
        #主演列表
        starrings = [AllActors.objects.get_or_create(name=name) for name in item['starring']]
         #类型列表
        types = [AllType.objects.get_or_create(type=t) for t in item['type']]
        #地区列表
        zones = [AllZone.objects.get_or_create(zone=z) for z in item['zone']]
        for pic in item['images'][1:]:
            pics.append(pic.get('path', ''))
        movie = Nanjing(
            title=item['title'][0].strip(),
            director=director[0],
            image_upload=','.join(pics),
            image_search=item['images'][0].get('path', ''),
            showtime='/'.join(item['showtime']),
            movie_time=item['movie_long'][0],
            score1=float(item['score1'][0]),
            score2=float(item['score2'][0]),
            summary=item['story'][0]
        )
        for z, b in zones:
            movie.zone = z
        #一个movie创建完成
        movie.save()

        for s, b in starrings:
            movie.starring.add(s)
        for t, b in types:
            movie.tags.add(t)

        #下载链接和资源大小
        downloads = [
            Links.objects.create(link=l, size=s, nanjing=movie) for l, s in zip(item['download'], item['size'])
        ]
        #保存Links外键关系
        director[0].directors.add(movie)
        director[0].save()
        for s, b in starrings:
            s.actors.add(movie)
            s.save()
        for t, b in types:
            t.movie_tags.add(movie)
            t.save()
        for z, b in zones:
            z.movie_zone.add(movie)
            z.save()
        for d in downloads:
            movie.download.add(d)
            movie.save()
        return item
