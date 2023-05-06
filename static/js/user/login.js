let vue=new Vue({
    el:'#login',
    delimiters:['%{','}'],
    data:{
       //v-model
       username:'',
       password:'',

       //v-show
       error_username:false,
       error_password:false,

       //v-message
       error_username_msg:'用户名错误',
       error_password_msg:'密码格式错误',

       qq_url:'',
    },mounted(){
       this.get_qq_url();
    },
    methods:{
         get_qq_url:function(){
             axios.get('/qq/login/',{
               responseType:'json'
             }).then(response=>{
               if(response.data.code=='200'){
                  this.qq_url=response.data.login_url;
               }
             }).catch(error=>{
               console.log(error.response)
             });
         }
    }


});