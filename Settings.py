# The Data Used For Login & Choosing Course
# By fengh16, 17.09.20 17:58

mUserName = "用户名"
mPassword = "密码"
mNowState = "2017-2018-1"
mWebBase = "http://zhjwxk.cic.tsinghua.edu.cn/"
mLogInWebSite = mWebBase + "xklogin.do"
mCaptchaWebSite = mWebBase + "login-jcaptcah.jpg?captchaflag=login1"
mLogInPost = mWebBase + "j_acegi_formlogin_xsxk.do"
mUrlBase = mWebBase + "xkBks.vxkBksXkbBs.do"
mCheckBase = mWebBase + "xkBks.vxkBksJxjhBs.do"
mChooseWebSiteFirstChoose = mUrlBase + "?m=selectKc&p_xnxq=" + mNowState + "&pathContent=%D2%BB%BC%B6%D1%A1%BF%CE"
mChooseWebSiteRX = mUrlBase + "?m=rxSearch&p_xnxq=" + mNowState + "&tokenPriFlag=rx&is_zyrxk=1"
mChosenCourse = mUrlBase + "?m=kbSearch&p_xnxq=" + mNowState + "&pathContent=%D2%BB%BC%B6%D1%A1%BF%CE%BF%CE%B1%ED"
mCheckLeft = mUrlBase + "?m=xkqkSearch&p_xnxq=" + mNowState
mWebDecoding = "gb2312"
mCaptchaPath = "C:\\Users\\username\\Desktop\\captchar\\pic.jpeg"
mCode = ""
content = ""
token = ""
mBlockList = [['00780461', '92'], ['00780461', '93']]
mNeedCourses = ['00780461']
mAlready = ""
