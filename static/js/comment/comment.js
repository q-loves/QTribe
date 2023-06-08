let vue=new Vue({
    el:'#form',
    delimiters:['${','}'],
    data:{

  },
    methods:{
        open_it:function(){
          let l_id = this.$refs.l_id.value
          console.log('l_id--->',l_id)
          this.$prompt('请输入评论', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /.+/,
          inputErrorMessage: '评论不可为空'
        }).then(({ value }) => {
            console.log('value--->',value)
            let url = '/pieces/comment_life/'
            let data_ = {'comment':value,'l_id':l_id}
            axios.post(url,data_).then(response=>{
                if(response.data.code==200){
                    this.$message({
                        type: 'success',
                        message: '发布成功哦'
                      });
                }else{
                    this.$message({
                        type: 'warning',
                        message: '发布失败'
                      });
                }
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          });
        });
        },

    }
});