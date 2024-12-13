
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Count
from django.db.models import Q
import datetime


# Create your views here.
from Remote_User.models import hybrid_feature_model,ClientRegister_Model,review_Model,recommend_Model,tweet_accuracy_model


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "robot" and password =="robot":
            tweet_accuracy_model.objects.all().delete()
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')


def viewtreandingquestions(request,chart_type):
    dd = {}
    pos,neu,neg =0,0,0
    poss=None
    topic = hybrid_feature_model.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('-dcount')
    for t in topic:
        topics=t['ratings']
        pos_count=hybrid_feature_model.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss=pos_count
        for pp in pos_count:
            senti= pp['names']
            if senti == 'positive':
                pos= pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics]=[pos,neg,neu]
    return render(request,'SProvider/viewtreandingquestions.html',{'object':topic,'dd':dd,'chart_type':chart_type})

def Search_Tweet(request): # Search
    if request.method == "POST":
        kword = request.POST.get('keyword')
        obj = hybrid_feature_model.objects.all().filter(Q(tweet_desc__contains=kword) | Q(names__contains=kword))
        return render(request, 'SProvider/Search_Tweet.html', {'objs': obj})
    return render(request, 'SProvider/Search_Tweet.html')

def View_Suicide_Retweets(request): # Using SVM
    sentiment='Suicide'
    f1 = 'suicide'
    f2 = 'death'
    f3 = 'sorrow'
    f4 = 'died'
    f5 = 'die'
    f6 = 'murder'
    f11 = 'fear'
    f22 = 'anxious'
    f33 = 'bored'
    f44 = 'alone'
    f55 = 'hang'
    f66 = 'hanged'

    obj1 = hybrid_feature_model.objects.all()
    obj = hybrid_feature_model.objects.all().filter(
        Q(retweet__contains=f1)| Q(retweet__contains=f2)| Q(retweet__contains=f3)| Q(retweet__contains=f4)|
        Q(retweet__contains=f5)| Q(retweet__contains=f6)| Q(retweet__contains=f11)|Q(retweet__contains=f22)|
        Q(retweet__contains=f33)|Q(retweet__contains=f44)|Q(retweet__contains=f55)|Q(retweet__contains=f66))

    count=obj.count()
    count1=obj1.count()
    accuracy=count/count1

    if accuracy !=0:
          tweet_accuracy_model.objects.create(names=sentiment,accuracy=accuracy)


    return render(request, 'SProvider/View_Suicide_Retweets.html', {'objs': obj,'count':accuracy})


def View_Positive_Retweets(request): # Positive # Using SVM
     sentiment='Positive'
     f1='good'
     f2='beautiful'
     f3='fantastic'
     f4='extraordinary'
     f5='best'
     f6='healthy'
     f7 ='happy'
     f8 = 'marvel'
     f9 = 'worth'
     f10 = 'value'
     f11='amazing'
     f12 = 'excellent'
     obj = hybrid_feature_model.objects.all().filter(Q(retweet__contains=f1) | Q(retweet__contains=f2)|Q(retweet__contains=f3) | Q(retweet__contains=f4)|Q(retweet__contains=f5) | Q(retweet__contains=f6)| Q(retweet__contains=f7)| Q(retweet__contains=f8)| Q(retweet__contains=f9)| Q(retweet__contains=f10)| Q(retweet__contains=f11)| Q(retweet__contains=f12))
     obj1 = hybrid_feature_model.objects.all()
     count = obj.count()
     count1 = obj1.count()
     accuracy = count / count1
     if accuracy != 0:
         tweet_accuracy_model.objects.create(names=sentiment, accuracy=accuracy)

     return render(request, 'SProvider/View_Positive_Retweets.html', {'objs': obj,'count':accuracy})

def View_Negative_Retweets(request): # Using SVM
    sentiment='Negative'

    f1 = 'bad'
    f2 = 'worst'
    f3 = 'heavy'
    f4 = 'ridicules'
    f5 = 'sad'
    f6 = 'damn'
    f7 = 'shameful'
    f8 = 'failed'
    obj = hybrid_feature_model.objects.all().filter(Q(retweet__contains=f1) | Q(retweet__contains=f2) | Q(retweet__contains=f3) | Q(retweet__contains=f4) | Q(retweet__contains=f5) | Q(retweet__contains=f6)| Q(retweet__contains=f7)| Q(retweet__contains=f8))
    obj1 = hybrid_feature_model.objects.all()
    count = obj.count()
    count1 = obj1.count()
    accuracy = count / count1
    if accuracy != 0:
        tweet_accuracy_model.objects.create(names=sentiment, accuracy=accuracy)

    return render(request, 'SProvider/View_Negative_Retweets.html', {'objs': obj,'count':accuracy})


def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = hybrid_feature_model.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def negativechart(request,chart_type):
    dd = {}
    pos, neu, neg = 0, 0, 0
    poss = None
    topic = hybrid_feature_model.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('-dcount')
    for t in topic:
        topics = t['ratings']
        pos_count = hybrid_feature_model.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss = pos_count
        for pp in pos_count:
            senti = pp['names']
            if senti == 'positive':
                pos = pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics] = [pos, neg, neu]
    return render(request,'SProvider/negativechart.html',{'object':topic,'dd':dd,'chart_type':chart_type})

def charts(request,chart_type):
    chart1 = tweet_accuracy_model.objects.values('names').annotate(dcount=Avg('accuracy'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def View_TweetDataSets_Details(request):
    obj = hybrid_feature_model.objects.all()
    return render(request, 'SProvider/View_TweetDataSets_Details.html', {'list_objects': obj})

def View_Sentiment_Accuracy(request):
    obj = tweet_accuracy_model.objects.all()
    return render(request, 'SProvider/View_Sentiment_Accuracy.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts = hybrid_feature_model.objects.values('names').annotate(dcount=Avg('tweet_score'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})






