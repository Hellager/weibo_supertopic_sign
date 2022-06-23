/*
 * @Author: Hellager
 * @Date: 2022-06-23 11:28:35
 * @LastEditTime: 2022-06-23 14:02:14
 * @LastEditors: Hellager
 * @Reference: https://segmentfault.com/a/1190000023356503
 */

var sharedArrayBuffer_for_sleep = new SharedArrayBuffer( 4 ) ;
var sharedArray_for_sleep = new Int32Array( sharedArrayBuffer_for_sleep ) ;

var sleep = function( n ) {
    Atomics.wait( sharedArray_for_sleep , 0 , 0 , n * 1000 ) ;
}

var usleep = function( n ) {
    Atomics.wait( sharedArray_for_sleep , 0 , 0 , n ) ;
}

module.exports = sleep;