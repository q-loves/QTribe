let vue = new Vue({
   el:'#form2',
   delimiters: ['${','}'],
   data:{
       // v-model
        username:'',
        email:'',
        age:'',
        signature:'',
        phone:'',

        // v-show
        error_username:false,
        error_email:false,
        error_age:false,
        error_signature:false,
        error_phone:false,

        // v-message
        error_username_msg:'请输入长度2-8的字符！',
        error_email_msg:'邮箱格式有误',
        error_phone_msg:'手机号输入有误！',
        error_age_msg:'年龄输入有误',
        error_signature_msg:'年龄输入有误',



   },
    methods:{


       // 校验用户名(只能输入2-8位字符)
        check_uname:function(){
            //1.格式校验
            let reg = /^[A-Za-z][A-Za-z0-9_]{2,7}$/;
            if(!reg.test(this.username)){
                this.error_username = true;
            }else{
                this.error_username = false;
            }

            //2.用户名是否重复注册校验
            if(!this.error_username){
                axios.get('/user/check_username/'+this.username+'/',{
                    responseType:'json'
                }).then(response=>{
                    if(response.data.count==1){
                        this.error_username_msg = '当前用户名已经注册';
                        this.error_username = true;
                    }else{
                        this.error_username = false;
                    }
                }).catch(error=>{
                    console.log(error.response);
                });
            }
        },
        //校验邮箱
        check_email:function(){
            let reg=/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$ /;
            if (!reg.test(this.phone)){
                this.error_email = true;
            }else{
                this.error_email = false;
            }
            //2.邮箱号是否重复校验
            if(!this.error_email){
                axios.get('/user/check_email/'+email+'/',{
                    responseType:'json'
                }).then(response=>{
                    if(response.data.count==1){
                        this.error_email_msg = '该邮箱号已被注册';
                        this.error_email = 'true';
                    }else{
                        this.error_email = 'false';
                    }
                }).catch(error=>{
                    console.log(error.response);
                });
            }
        },
        //校验年龄
        check_age:function(){
          let reg = /^((1[0-5])|[1-9])?\d$/;
          if(!reg.test(this.age)){
            this.error_age = true;
          }else{
            this.error_age = false;
          }
        },

        // 校验手机号
        check_phone:function(){
            // 1.格式校验
            let reg = /^1[3,5,7,8,9]\d{9}$/;
            if(!reg.test(this.phone)){
                this.error_phone = true;
            }else{
                this.error_phone = false;
            }

            // 2.手机号是否重复注册校验
            if(!this.error_phone){
                axios.get('/user/check_phone/'+this.phone+'/',{
                    responseType:'json'
                }).then(response=>{
                    if(response.data.count==1){
                        this.error_phone_msg = '手机号已经被注册';
                        this.error_phone = true;
                    }else{
                        this.error_phone = false;
                    }
                }).catch(error=>{
                    console.log(error.response);
                });
            }
        },
        // 监听表单提交事件
        reg_sub:function(){
            this.check_uname();
            this.check_phone();

            if(this.error_username||this.error_phone||this.error_email){
                //阻止表单提交
                window.event.returnValue = false;
            }
        }

    }
});
