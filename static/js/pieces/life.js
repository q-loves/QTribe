let vue=new Vue({
    el:'#form',
    delimiters:['${','}'],
    data:{


       //v-model
      content:'',


       //v-show
       error_content:false,
       error_form:false,
       //v-message
       error_content_msg:'请输入文案',
       error_form_msg:'请完善表单内容',


  },

    methods:{

              //上传文章成功或失败后，弹出弹窗
              uploadFile:function(){

                    this.check_content();
                    const formData = new FormData();
                    const file = this.$refs.fileInput.files;
                    if(!this.error_content && file){
                        this.error_form=false;

                        for(var i=0;i<this.$refs.fileInput.files.length;i++){
                            formData.append('image', this.$refs.fileInput.files[i]);
                        }

                        formData.append('remark',this.content);
                        axios.post('/pieces/share_life/',formData).then(response=>{
                            if(response.data.code==200){
                                swal('发布成功');
                                window.location.href = '/pieces/share_life/';
                            }else{
                                swal('发布失败');
                            }
                        });
                    }else{
                        this.error_form=true;
                    }

              },


            //校验文案
            check_content:function(){
                let reg =/^.{1,512}$/;
                if(!this.content){
                    this.error_content_msg='文案不可为空';
                    this.error_content = true;
                }else{
                    this.error_content = false;
                    if(!reg.test(this.content)){
                        this.error_content_msg='文案不能超过512个字';
                        this.error_content = true;
                    }else{
                        this.error_content=false;
                    }

                 }

          },


 }
});