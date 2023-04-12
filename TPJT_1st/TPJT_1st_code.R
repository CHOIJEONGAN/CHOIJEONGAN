suwon=as.data.frame(read_excel("수원시 데이터(원본).xlsx"))
su1=as.data.frame(read_excel("수원시 데이터(수정).xlsx"))
# 데이터 확인
View(suwon)

# 수원시 지역별 범죄수 선그래프
ggplot(data = suwon, aes(x=year, y=onehouse, colour=location))+
  geom_line(lwd=2)+
  ggtitle('수원시 1인 가구')+
  theme(plot.title = element_text(hjust = 0.5,size=20,face='bold'))+
  theme_bw()


plot(su$year, su$people,main='수원시 정보',
     type="b", lty=1, lwd=2,
     xlab='연도', ylab='',ylim=c(0,1300000))
lines(su$year, su$police, type="b", lty=1,col='blue')
lines(su$year, su$crime,type="b", lty=1,col='red')

plot(su$year, su$crime,main='수원시 범죄',
     type="b", lty=1, lwd=2,
     xlab='연도', ylab='',ylim=c(0,15000), col='red')
lines(su$year, jang$crime, type="b", lty=1,col='blue')
lines(su$year, pal$crime, type="b", lty=1,col='green')
lines(su$year, young$crime, type="b", lty=1,col='orange')
lines(su$year, gwon$crime, type="b", lty=1,col='pink')

round(cor(su[,-c(1,2,12,13)], method = "spearman"),4)


mod1=lm(crime~cctv+police+store+student+onehouse+0,data=gwon)
mod2=step(mod1, direction = "both",trace=F)
summary(mod2)
cor(su$crime,su$steerlight)
pairs(~crime+cctv+steerlight+police+store+school+student+onehouse,data=su)
# crime = 8.660e+01 + 6.287e-03*people - 6.405e-01*cctv - 2.011e-01*steerlight + 8.438e+00*police
#crime = ??? 0.447*police +0.066*student
su
test=su[8:10,-c(3,12,13)]
test
test1=suwon[47:50,4:11]
test1

pred=predict(mod2,test)
pred1=predict(mod2,test,interval = 'confidence')
pred2=predict(mod2,test, interval = 'prediction')
test
w
pred
pred1
pred2
w=su[8:10,3]

bind=cbind(test$year,test$location, w,round(pred1,2))
bind=as.data.frame(bind)
bind
c=bind
names(c)=c('year', 'location','crime','pred','lwr','upr')
c
c[3,3]=NA


test1= 
  # 잔차분석
  plot(mod1)


par(mfrow=c(2,2))


#위험등급
as=suwon[order(suwon$year,decreasing = F),]
as
danger=as[41:50,-c(3:11)]
danger




#안전지수 가중치
#safe=50*rate_crime+1.7*people+3.04*rate_store+5.26*onehouse-17.16*rate_police-2.71*rate_cctv-0.13*rate_steerlight
rbind(a,dong)
a=as.data.frame(suwon %>%
                  mutate(danger=(60*rate_crime+2.7*people
                                 +4.04*rate_store+6.26*onehouse-18.16*rate_police
                                 -4.71*rate_cctv-2.13*rate_steerlight)/10000) 
)
a
#사분위수 확인
quantile(a$safety,seq(0,1,by=0.2))

danger=c()                  # safe의 벡터변수 지정(Null 값)
for(i in 1:54){               # 반복문 실행
  if (a$danger[i]<=25){         # 조건 1
    danger[i] ='1등급'         # 결과 1
  } else if (a$danger[i]<=50){      # 조건 2
    danger[i] = '2등급'         # 결과 2
  } else if (a$danger[i]<=75){      # 조건 3
    danger[i] = '3등급'         # 결과 3    
  } else if (a$danger[i]<=100){      # 조건 4
    danger[i] = '4등급'         # 결과 4
  } else if (a$danger[i]<=150){      # 조건 5
    danger[i] = '5등급'         # 결과 5 
  } else {            
    danger[i] = ''      # 결과 6    
  }
}
danger
b=cbind(a$year,a$location,w,round(a$rate_crime,2),danger)
b=as.data.frame(b)
names(b)=c('year','location','rate_crime','safety')
print(b)
safety=b[order(b$year,decreasing = F),]
safety=safety[41:54,]
safety=safety[-c(2,7),]
safety

test1=