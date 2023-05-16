let vue = new Vue({
   el:'#form',
   delimiters: ['${','}'],
   data:{
       // v-model
        username:'',
        password:'',
        smscode:'',
        phone:'',

        // v-show
        error_username:false,
        error_password:false,
        error_phone:false,
        error_smscode:false,

        // v-message
        error_username_msg:'请输入长度2-8的字符！',
        error_password_msg:'请输入长度8-16的字符！',
        error_phone_msg:'手机号输入有误！',
        error_smscode_msg:'验证码输入有误！',

       //短信验证码相关变量
       smscode_btn:'发送验证码',
       send_flag:false,

   },
    methods:{
       send_smscode:function(){
           //发送短信验证码
           //1.判断短信验证码是否正在发送
           if(this.send_flag){
               return;
           }

           //2.修改发送状态
           this.send_flag = true;

           //3.校验用户输入的手机号
           this.check_phone();
           if(this.error_phone){
               this.send_flag = false;
               return;
           }

           //4.发送短信验证码
           var url = '/code/send_smscode/'+this.phone+'/';
           axios.get(url,{
               responseType:'json'
           }).then(response=>{
               if(response.data.code=='200'){
                   let num = 60;
                   var i = setInterval(()=>{
                       if(num==1){
                           clearInterval(i);
                           this.smscode_btn = '获取短信验证码';
                           this.send_flag = false;
                       }else{
                           num -= 1;
                           this.smscode_btn = '倒计时：'+ num + '秒';
                       }
                   },1000,60)
               }else{// 4001 表示缺少必传参数
                   if(response.data.data =='4001' ||response.data.data =='4002' ||response.data.data =='4003'){
                       this.error_smscode_msg = response.data.errormsg;
                       this.error_smscode = true;
                       // 4002 图片验证码已经过期
                   }
                   //重置发送状态
                   this.send_flag = false;
               }
           }).catch(error=>{
               console.log(error.response);
           });

       },
       check_smscode:function(){
           //短信验证码格式校验
//           let reg = /^\d{6}$/;
           let reg = /\d{6}/;
           console.log("this.smscode",this.smscode);
           console.log("reg.test",typeof(reg.test(this.smscode)));


           if(!reg.test(this.smscode)){
            console.log('11111111111');
               this.error_smscode = true;
           }else{
                console.log("true")
               this.error_smscode = false;
           }


           if(!this.error_smscode){
              axios.get('/code/check_smscode/'+this.phone+'/?smscode='+this.smscode).then(response=>{
              let code=response.data.code
              if(code!=200){
                  this.error_smscode=true;
                  this.error_smscode_msg=response.data.errormsg;

              }else{
              this.error_smscode=false

              }
              });
           }
       },

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
        // 校验密码
        check_pwd:function(){
            let reg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$/;
            if(!reg.test(this.password)){
                this.error_password = true;
            }else{
                this.error_password = false;
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
            this.check_pwd();
            this.check_smscode();

            if(this.error_username||this.error_phone||this.error_password||this.error_smscode){
                //阻止表单提交
                window.event.returnValue = false;
            }
        }

    }
});
