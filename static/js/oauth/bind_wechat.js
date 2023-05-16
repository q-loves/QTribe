let vue = new Vue({
   el:'#form',
   delimiters: ['${','}'],
   data:{
       // v-model
        password:'',
        smscode:'',
        phone:'',
//        sec_openid:'',

        // v-show
        error_password:false,
        error_phone:false,
        error_smscode:false,
        error_form:false,

        // v-message
        error_password_msg:'请输入长度8-16的字符！',
        error_phone_msg:'手机号输入有误！',
        error_smscode_msg:'验证码输入有误！',
        error_form_msg:'请完善表单！',



       //短信验证码相关变量
       smscode_btn:'获取短信验证码',
       send_flag:false,

   },
    methods:{

            bind_qq:function(){
//                      swal('成功');

                    this.check_pwd();
                    this.check_phone();
                    this.check_smscode();
                    let openid = this.$refs.sec_openid.value
                    if(this.error_smscode||this.error_phone||this.error_phone){
                        this.error_form=true;
                    }else{
                        this.error_form=false;
                        let data = {'phone':this.phone,'smscode':this.smscode,'password':this.password,'sec_openid':openid}
                        axios.post('/about/',data).then(response=>{
                            if(response.data.code==200){
                                  //跳转到主页面
                                  window.location.href = '/index/home_index/';
                            }else{
                                swal('绑定失败');
                            }
                        });
                    }
            },
            check_pwd:function(){
                    if (!this.password){
                        this.error_password_msg='密码不可为空';
                        this.error_password = true;

                    }else{
                        let data = {'phone':this.phone,'password':this.password}
                        axios.post('/user/check_password/',data).then(response=>{
                            if(response.data.code==200){
                                this.error_password=false;
                            }else{
                                this.error_password_msg='电话号或密码错误';
                                this.error_password=true;

                            }
                        });
                    }
             },
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
               let reg = /^\d{6}$/;
               if(!reg.test(this.smscode)){
                   this.error_smscode = true;
               }else{
                   this.error_smscode = false;
               }
               if(!this.error_smscode){
                  console.log('111111');
                  axios.get('/code/check_smscode/'+this.phone+'/?smscode='+this.smscode ).then(response=>{

                  let code=response.data.code;
                  console.log('code',code)
                  if(code!=200){
                      this.error_smscode_msg=response.data.errormsg;
                      this.error_smscode=true;

                  }else{

                  this.error_smscode=false

                  }
                  });
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

                // 2.查看是否有对应手机号的用户
                if(!this.error_phone){
                    axios.get('/user/check_phone/'+this.phone+'/',{
                        responseType:'json'
                    }).then(response=>{
                        if(response.data.count!=1){
                            this.error_phone_msg = '该手机号未绑定用户，请先注册';
                            this.error_phone = true;
                        }else{
                            this.error_phone = false;
                        }
                    }).catch(error=>{
                        console.log(error.response);
                    });
                }
            },


}
});