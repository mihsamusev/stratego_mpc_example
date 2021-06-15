strategy opt = minE (D) [<=5*15]: <> (t==1500.0)

simulate 1 [<=15+1] { t,T,D,heatLoc,winLoc,w,i } under opt
