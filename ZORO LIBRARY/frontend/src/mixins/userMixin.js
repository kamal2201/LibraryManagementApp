export default {
    data() {
        return {
            user: null,
            email: null,
            isloggedin: false
        }
    },
    async created(){
        await this.checkUserStatus();
    },
    methods: {
        async checkUserStatus() {
            const token = localStorage.getItem('access_token');
            if (!token){
                this.user = null;
                this.email = null;
                this.isloggedin = false;
                return;
            }
            try{
                this.user = await this.getUserInfo();
                this.email = this.user.email;
            }
            catch(error){
                this.user = null;
                this.email = null;
                this.isloggedin = false;
                console.log("Error while fetching user info: ",error);
                return;
            }
        },
        async getUserInfo() {
            const token = localStorage.getItem('access_token');
            console.log(token)
            const response = await fetch('http://127.0.0.1:5000/getuserinfo', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            console.log(data)
            if (!response.ok){
                this.isloggedin = false;
                return null
            }
            this.isloggedin = true;
            return data;
        },
        logout() {
            fetch('http://127.0.0.1:5000/logout', {
                method: 'POST',
                credentials:'include'
            })
            .then(() => {
                localStorage.removeItem('access_token');
                this.user = null;
                this.email = null;
                this.isloggedin = false;
                this.$router.push('/login');
            })
            .catch((error) => {
                console.log("Logout Error",error);
            });
        }  
    },

}