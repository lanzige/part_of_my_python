import downloadURL
import itertools

if __name__=="__main__":
    max_error=5
    num_error=0
    for page in itertools.count(3927547):
        url="http://www.acfun.cn/a/ac%d"%(page)
        html=downloadURL.download(url)
        if html is None:
            num_error+=1
            if num_error==max_error:
                break
        else:
            pass