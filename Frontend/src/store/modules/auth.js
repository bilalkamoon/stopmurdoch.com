import axios from 'axios';
const state = {
  user: null,
  admin: null,
  error: "",
  votingError: "",
  registerError: "",
  listCandidates: [],
  UsersToVerify: [],
  loginError: "",
  elections: [],
  currentElection: null,
  isAdmin: false
};
const getters = {
   isAuthenticated: state => !!state.user,  
   isAdminAuthenticated: state => !!state.admin,
   StateUser: state => state.user,
   StateAdmin : state => state.admin
};
const actions = {
async SetCurrentElection({dispatch}, election){
   dispatch('SetCurrentElection', election)
},
async SetCurrentElection({commit}, election){
   commit('SetCurrentElection', election)
},
async AddNewElection({dispatch}, form){
  await axios.post("AddNewElection", form);
},
async TryVote({dispatch}, values){
  const form = new FormData();
  form.append("candidateId", values[1]);
  form.append("username", values[0]);
  form.append("fingerprint", values[2]);
  form.append("score", values[3]);
  await axios.post("Vote", form).then((response) =>{
     dispatch("Vote", response.data)
      
  });
},
async Vote({commit}, data){
  if("error" in data){
          commit('setVotingError',data.error);
      }else{
          commit('setVotingError', "")
      }
},
async DenyUser({dispatch}, userName){
  const form = new FormData();
  form.append("userName", userName);
  await axios.post("DenyUser", form);
},
async VerifyUser({dispatch}, userName){
  const form = new FormData();
  form.append("userName", userName);
  await axios.post("VerifyUser", form);
},
async SetCandidatesList({commit}, l){
  await commit('SetCandidatesList', l)
},
async getElections({dispatch}){
  await axios.post('getElections').then((response)=>{
      dispatch('SetElections', response.data.rows);
  });

},
async SetElections({commit}, d){
 await commit("SetElections", d)
},
async SetUsersToVerifyList({commit}, l){
 await commit('SetUsersToVerifyList', l)
},
async EndElection({dispatch}, form){
  await axios.post('EndElection', form);
},
async GetUsersToVerify({dispatch}){
  await axios.post('getUsersToVerify').then((response) =>{
    dispatch('SetUsersToVerifyList', response.data.rows);
  })
},
async GetCandidatesList({dispatch}, election){
  let form = new FormData();
   form.append('electionId', election.electionId)
   form.append('includeVotes', !election.isOngoing)

 await axios.post('getCandidatesList', form).then((response) =>{
    dispatch('SetCandidatesList', response.data.rows);
 })
},
async AddNewCandidate({dispatch}, form){
  await axios.post('addNewCandidate', form,{headers: {
      'Content-Type': 'multipart/form-data'
    }})
},
   async Register({dispatch}, form) {
   let RegisterForm = new FormData()
  RegisterForm.append('username', form.username)
  RegisterForm.append('password', form.password)
  RegisterForm.append('fingerprint', form.fingerprint)
  RegisterForm.append('full_name', form.full_name)
  await axios.post('register', RegisterForm).then((response) =>{
       dispatch("RegisterCommit", response.data);
  });
},
async RegisterCommit({commit},data){
 if("error" in data){
          commit('setRegisterError',data.error);
      }else{
          commit('setRegisterError', "")
      }
},
async LogIn({commit}, User) {
  await axios.post('Login', User).then((response) =>{
     if("error" in response.data){
         commit('setUser', null)
     	  commit('setLoginError', response.data.error)
     }else{
     	commit('setUser', User.get('username'))
     	commit('setLoginError', "")
     	commit('setIsAdmin', response.data.data);
     	}
  });
},async LogOut({commit}){
  commit('LogOut')
}

};
const mutations = {
SetCandidatesList(state, listCandidates){
 state.listCandidates = listCandidates
},
 setUser(state, username){
        state.user = username
    },setAdmin(state, username){
        state.admin = username
    },LogOut(state){
        state.user = null
        state.admin = null
    },setError(state, error){
       state.error = error;
    },setRegisterError(state, error){
       state.registerError = error;
    },SetUsersToVerifyList(state, l){
      state.UsersToVerify = l;
    },setLoginError(state,error){
      state.loginError = error;
    },
    setIsAdmin(state, isAdmin){
       state.isAdmin = isAdmin
    },
     SetElections(state, d){
      state.elections = d
    }, SetCurrentElection(state, election){
      state.currentElection = election
    }, setVotingError(state, error){
      state.votingError = error
    }
};
export default {
  state,
  getters,
  actions,
  mutations
};
