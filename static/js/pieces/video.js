let vue=new Vue({
    el:'#form',
    delimiters:['${','}'],
    data:{

      video:'',
       //v-model
      title:'',
      remark:'',


       //v-show
       error_title:false,
       error_remark:false,
       error_form:false,

       //v-message
       error_title_msg:'标题过长',
       error_remark_msg:'视频描述过长',
       error_form_msg:'请完善表单信息',


  },

    methods:{
              open1:function() {
                    this.$notify({
//                      title: '成功',
                      message: '视频上传成功',
                      type: 'success'
                    });
                  },
              open2:function() {
                this.$notify.error({
//                  title: '错误',
                  message: '视频上传失败'
                });
              },
              //上传视频成功或失败后，弹出弹窗
              uploadFile:function(){

                    this.check_title();
                    this.check_remark();
                    const formData = new FormData();
                    const file = this.$refs.fileInput.files[0];
                    //判断表单是否填写完整
                    if(!this.error_title && !this.error_remark && file){
                        this.error_form=false;

                        formData.append('video', file);
                        formData.append('title',this.title);
                        formData.append('remark',this.remark);
                        let url = '/pieces/upload_video/';

                        axios.post(url,formData).then(response=>{
                            if(response.data.code==200){

                                  swal('视频上传成功');
                                  window.location.href = '/pieces/upload_video/';
                            }else{

                                  swal('视频上传失败');
                            }
                        });
                    }else{
                        this.error_form=true;
                    }

              },

            //校验标题
            check_title:function(){
                let reg =/^.{1,20}$/;
                if(!this.title){
                    this.error_title_msg='标题不可为空';
                    this.error_title = true;
                }else{
                     if(!reg.test(this.title)){
                            this.error_tile_msg='标题字数不可超过20';
                            this.error_title = true;
                         }else{
                            this.error_title = false;
                        }

                 }

          },
            //校验视频描述
            check_remark:function(){
                let reg =/^.{1,50}$/;
                if(!this.remark){
                    this.error_remark_msg='描述不可为空';
                    this.error_remark = true;
                }else{
                    if(!reg.test(this.remark)){
                        this.error_remark_msg='描述字数不可超过50';
                        this.error_remark = true;

                     }else{
                        this.error_remark = false;
                  }

                 }

          },


 }
});