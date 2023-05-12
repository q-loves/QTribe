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
        error_submit:false,
        // v-message
        error_username_msg:'请输入长度2-8的字符！',
        error_email_msg:'邮箱格式有误',
        error_phone_msg:'手机号输入有误！',
        error_age_msg:'年龄输入有误',
        error_signature_msg:'年龄输入有误',
        error_submit_msg:'请完善表单',


   },
    methods:{
        open:function(){
            this.$prompt('请输入新密码', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$/,
          inputErrorMessage: '密码格式不正确'
        }).then(({ value }) => {
            let url = '/user/reset_password/'
            axios.post(url,{'password':value}).then(response=>{
                if(response.data.code==200){
                    this.$message({
                        type: 'success',
                        message: '你修改后的密码是: ' + value
                      });
                }else{
                    swal('修改失败');
                }
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
        },
        resetPassword:function(){
             this.$prompt('请输入原密码', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',

        }).then(({ value }) => {
          let url = '/user/reset_password/?password='+value
          axios.get(url).then(response=>{
            if(response.data.code==200){
                console.log('成功')
                this.open();
            }else{
                swal('密码错误');
            }
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
        },
        submit_:function(){
            this.check_age();
            this.check_email();
            this.check_phone();
            this.check_uname();
            let data={'username':this.username,'phone':this.phone,'email':this.email,'age':this.age,'personalized_signature':this.signature} ;
            let url = '/user/update_information/';
            if(this.error_age||this.error_email||this.error_phone||this.error_username){
                    this.error_submit=true;
            }else{
                   axios.post(url,data).then(response=>{
                        if(response.data.code==200){
                            swal('保存成功');
                        }else{
                            swal('保存失败');
                        }
                    });
            }
        },
       // 校验用户名(只能输入2-8位字符)
        check_uname:function(){
            if(!this.username){
                this.error_username=false;
            }else{
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
        }
            }
            ,

        //校验年龄
        check_age:function(){

            if(!this.age){
                this.error_age=false;
            }else{
                 let reg = /^((1[0-5])|[1-9])?\d$/;
              if(!reg.test(this.age)){
                this.error_age = true;
              }else{
                this.error_age = false;
              }
            }
            }
             ,

        // 校验手机号
        check_phone:function(){

            if(!this.phone){
                this.error_phone=false;
            }else{
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
        }
            }
           ,
       // 校验邮箱
        check_email:function(){

            if(!this.email){
                this.error_email=false;
            }else{

            // 2.邮箱是否重复注册校验
            if(!this.error_email){
                axios.get('/user/check_email/'+this.email+'/',{
                    responseType:'json'
                }).then(response=>{
                    if(response.data.count==1){
                        this.error_email_msg = '邮箱号已经被注册';
                        this.error_email = true;
                    }else{
                        this.error_email = false;
                    }
                }).catch(error=>{
                    console.log(error.response);
                });
            }
        }
            }
           ,

    }
});
