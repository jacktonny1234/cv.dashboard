"use client"

// Import the axios library
import axios from 'axios';

// const API_SERVER_URL = process.env.API_SERVER_URL;
const API_SERVER_URL = "http://142.132.222.204:8888/api/v1/";
// const API_SERVER_URL = "http://192.168.153.128:8888/api/v1/";

const $ = {
    // Make the POST request using the async/await syntax
    post: function (url: string, data: any, cb_ok: any = null,  cb_error:any = null){
            const fullUrl = API_SERVER_URL + url;
            console.log('Making POST request to:', fullUrl);
            console.log('Request data:', data);
            
            axios.post(
                fullUrl, 
                data, 
                { 
                    headers: {
                        "Content-Type": "application/json"
                    },
                    withCredentials: false
                }
            ).then((response) => {
                console.log('POST request successful:', response.status);
                if( cb_ok )
                    cb_ok(response);
            }).catch((error) => {
                console.error('POST request failed:', error);
                console.log(`Error message: ${error.message}`);
                console.log(`Error code: ${error.code}`);
                console.log(`Error response:`, error.response);
                if (cb_error)
                    cb_error(error);
            });
    },
    // Make the POST request using the async/await syntax
    upload: function (url: string, data: any, file:any, cb_ok: any = null,  cb_error:any = null){
        axios.post(API_SERVER_URL + url, data,
            { 
                headers: {
                "Content-Type": "multipart/form-data"
                }
            }
        ).then((response) => {
            if( cb_ok )
                cb_ok(response);
        }).catch((error) => {
            if (cb_error)
                cb_error(error);
            console.log(`Error message: ${error.message}`);
            console.log(`Error code: ${error.code}`);
        });
}
}

export default $;