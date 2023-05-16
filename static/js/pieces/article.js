let vue=new Vue({
    el:'#form',
    delimiters:['${','}'],
    data:{


       //v-model
      title:'',
      content:'',


       //v-show
       error_title:false,
       error_content:false,
       error_form:false,
       //v-message
       error_title_msg:'',
       error_content_msg:'请输入文章',
       error_form_msg:'请完善表单内容',


  },

    methods:{
              open1:function() {
                    this.$notify({
//                      title: '成功',
                      message: '上传成功',
                      type: 'success'
                    });
                  },
              open2:function() {
                this.$notify.error({
//                  title: '错误',
                  message: '上传失败'
                });
              },
              //上传文章成功或失败后，弹出弹窗
              uploadFile:function(){

                    const formData = new FormData();
                    const file = this.$refs.fileInput.files[0];
                    if(!this.error_title && !this.error_content && file){
                        this.error_form=false;

                        for(var i=0;i<this.$refs.fileInput.files.length;i++){
                            formData.append('image', this.$refs.fileInput.files[i]);
                        }
                        formData.append('title',this.title);
                        formData.append('content',this.content);
                        console.log('file---->',formData)
                        axios.post('/pieces/publish_article/',formData).then(response=>{
                            if(response.data.code==200){
                                swal('文章上传成功');
                            }else{
                                swal('文章上传失败');
                            }
                        });
                    }else{
                        this.error_form=true;
                    }

//                    let url = '/pieces/upload_article/';
//
//                    axios.post(url,formData).then(response=>{
//                        if(response.data.code==200){
//
//                              this.open1();
//                        }else{
//
//                              this.open2();
//                        }
//                    });
              },

            //校验标题
            check_title:function(){
                let reg =/^.{1,100}$/;
                if(!this.title){
                    this.error_title_msg='标题不可为空';
                    this.error_title = true;
                }else{
                     if(!reg.test(this.title)){
                            this.error_tile_msg='标题字数不可超过100';
                            this.error_title = true;
                         }else{
                            this.error_title = false;
                        }

                 }

          },
            //校验视频描述
            check_content:function(){
                if(!this.content){
                    this.error_content_msg='文章不可为空';
                    this.error_content = true;
                }else{
                    this.error_content = false;

                 }

          },


 }
});