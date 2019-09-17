<template>
  <div class='container'>
    <div class="row">
      <div class="col-sm-10">
        <h1>Polls</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button"
                class="btn btn-success btn-sm"
                v-b-modal.poll-modal>Add Poll</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Question</th>
              <th scope="col">Votes</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(poll, index) in polls" :key="index">
              <td>{{ poll.question.substr(-1) == '?' ? poll.question : poll.question + '?'  }}
                <ul class='list-group'>
                  <li v-for="option in poll.options"
                      :id="`option-${option.answer_id}`"
                      :class='option.active ? "list-group-item active" : "list-group-item"'
                      @click="pollVote(option,poll.poll_id)">
                    {{ option.answer }}
                  </li>
                </ul>
              </td>
              <td>Totals
                <ul class='list-group'>
                  <li v-for="option in poll.options"
                      :id="`option-${option.answer_id}`"
                      :class='option.most_votes ? "list-group-item list-group-item-success" : "list-group-item"'>
                    {{ option.votes.length }}
                  </li>
                </ul>

              </td>
              <td>
                <div class="btn-group" role="group">
                  <button v-if='poll.voted'
                          type="button"
                          class="btn btn-success btn-sm"
                          @click="pollDetail(poll)"
                          v-b-modal.detail-modal>Details</button>
                   <button v-if='poll.editable'
                          type="button"
                          class="btn btn-warning btn-sm">Mine</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  <b-modal ref="addPollModal"
           id="poll-modal"
           title="Add a new poll"
           hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-question-group"
                    label="Question:"
                    label-for="form-question-input">
        <b-form-input id="form-question-input"
                      type="text"
                      v-model="addPollForm.question"
                      required
                      placeholder="Poll question">
        </b-form-input>
      </b-form-group>
      <div>
        <label>Options:</label>
        <b-form-group v-for="option in addPollForm.answers"
                      class='optionArea'
                      :key="option.id">
          <b-form-input v-model="option.answer"
                        type='text'
                        :id="option.id"
                        :placeholder="option.placeholder"></b-form-input>
        </b-form-group>
        <b-button @click="addAnswer">Add Option</b-button>
      </div>
      <b-button-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset"  variant="danger">Reset</b-button>
      </b-button-group>
    </b-form>
  </b-modal>
  <b-modal ref="pollDetail"
           id="detail-modal"
           :title="details.title"
           hide-footer>
    <pre>{{ details.voters }}</pre>

  </b-modal>

<!--   <b-modal ref="editPollModal"
           id="poll-edit-modal"
           title="Edit"
           hide-footer>
    <b-form @submit="onSubmitEdit" @reset="onResetEdit" class="w-100">
    <b-form-group id="form" -->

  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      polls: [],
      addPollForm: {
        question: '',
        answers: [],
      },
      details: {
        title: 'Poll Details',
        voters: {},
      },
      answer_count: 0,
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getPolls() {
      const path = 'http://localhost:5000/polls';
      axios.get(path)
        .then((res) => {
          this.polls = res.data;
          // console.log(this.polls)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addPoll(payload) {
      const path = 'http://localhost:5000/create?question=';
      axios.post(path + payload.question, payload)
        .then(() => {
          this.getPolls();
          this.message = 'Poll added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getPolls();
        });
    },
    pollVote(option, pollId,el) {
      const path = `http://localhost:5000/poll/${pollId}/?answer_id=${option.answer_id}`;
      this.isActive = true;
      axios.post(path, option)
        .then(() => {
          this.getPolls();
          this.message = 'Vote recorded!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getPolls();
        });
    },
    pollDetail(poll){
      this.details.title = poll.question + ' Vote Details';
      this.details.voters = poll.options.map(option => {
        var opt = {
          answer: option.answer,
          votes: option.votes,
        };
        return opt;
      });
    },
    addAnswer() {
      this.addPollForm.answers.push({
        id: `answer-${this.answer_count}`,
        placeholder: `Poll Option ${(this.answer_count + 1)}`,
        answer: '',
      });
      this.answer_count += 1;
    },
    initForm() {
      this.addPollForm.question = '';
      this.addPollForm.answers = [];
      this.answer_count = 0;
      this.addAnswer();
      this.addAnswer();
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addPollModal.hide();
      const payload = {
        question: this.addPollForm.question,
        answers: this.addPollForm.answers.map(a => a.answer),
      };
      this.addPoll(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addPollModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getPolls();
  },
  mounted() {
    this.addAnswer();
    this.addAnswer();
  },
};

</script>
