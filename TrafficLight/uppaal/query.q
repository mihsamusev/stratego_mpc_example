//This file was generated from (Academic) UPPAAL 4.1.20-stratego-7 (rev. 12D93ED5FE521036), December 2019

/*

*/
strategy opt = minE(Q) [<=HORIZON]:<>time>=HORIZON

/*

*/
simulate 1 [<=HORIZON] {phase} under opt

/*

*/
E[<=HORIZON;500] (max: Q)

/*

*/
E[<=HORIZON;500] (max: Q) under opt

/*

*/
//NO_QUERY
