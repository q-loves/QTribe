let vue=new Vue({
    el:'#form',
    delimiters:['${','}'],
    data:{


  },
    methods:{

        focus:function(){

            let url = '/user/focus/?o_id='+this.$refs.inputId.value+'&is_focus=1';
            axios.get(url).then(response=>{
                if(response.data.code==200){
                    window.location.href = '/index/other_user/';
                }else{
                    swal('关注失败');
                }
            });
        },
        unfocus:function(){
            let url = '/user/focus/?o_id='+this.$refs.inputId.value+'&is_focus=0';
            axios.get(url).then(response=>{
                if(response.data.code==200){
                    window.location.href = '/index/other_user/';
                }else{
                    swal('取消关注失败');
                }
            });
        },
        focus2:function(){

            let url = '/user/focus/?o_id='+this.$refs.inputId.value+'&is_focus=1';
            let current_page = this.$refs.currentPage.value;
            let q = this.$refs.q.value;
            axios.get(url).then(response=>{
                if(response.data.code==200){
                    window.location.href = '/index/search_user/?current_page='+this.current_page+'&q='+this.q;
                }else{
                    swal('关注失败');
                }
            });
        },
        unfocus2:function(){
            let url = '/user/focus/?o_id='+this.$refs.inputId.value+'&is_focus=0';
            axios.get(url).then(response=>{
                if(response.data.code==200){
                    window.location.href = '/index/search_user/?current_page='+this.current_page+'&q='+this.q;
                }else{
                    swal('取消关注失败');
                }
            });
        },

    },

});