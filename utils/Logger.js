/*
 * @Author: Hellager
 * @Date: 2022-06-20 15:21:22
 * @LastEditTime: 2022-06-23 14:01:52
 * @LastEditors: Hellager
 */

const dayjs = require('dayjs');

class Logger {
    constructor () {

    }

    info(msg) {
        const current_time = dayjs().format('YYYY-MM-DD HH:mm:ss');
        console.log(`${current_time} info ${msg}`);
    }

    warning(msg) {
        const current_time = dayjs().format('YYYY-MM-DD HH:mm:ss');
        console.log(`${current_time} warning ${msg}`);       
    }

    error(msg) {
        const current_time = dayjs().format('YYYY-MM-DD HH:mm:ss');
        console.log(`${current_time} error ${msg}`);            
    }
}

log = new Logger();

module.exports = log;
