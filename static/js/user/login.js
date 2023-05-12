let vue=new Vue({
    el:'#form',
    delimiters:['${','}'],
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


  },

    methods:{


     check_uname:function(){
            if(!this.username){
                this.error_username = true;
                this.error_username_msg='用户名不可为空'
            }else{
                this.error_username = false;
            }
     },
     check_pwd:function(){
            if (!this.password){
                this.error_password = true;
                this.error_password_msg='密码不可为空'
            }else{
                this.error_username = false;
            }
     },
      // 监听表单提交事件
        reg_sub:function(){
            this.check_uname();
            this.check_pwd();

            if(this.error_username||this.error_password){
                //阻止表单提交
                window.event.returnValue = false;
            }
        }


    }
});