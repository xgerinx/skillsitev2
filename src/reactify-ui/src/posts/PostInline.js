import React, {Component} from 'react';
import Windows from '../Windows';
import Modal from "../Modals/Auth";

class PostInline extends Windows {

    render() {
        const {post} = this.props;
        const {elClass} = this.props;
        const showContent = elClass === 'card' ? 'd-block' : 'd-none';
        console.log(post);
        return (
            <div onClick={this.toggleModal}>
                {post !== undefined ? <div className={elClass} onClick={this.toggleBuy}>
                        <h1>{post.title}</h1>
                        <p className={showContent}>{post.content}</p>
                    </div>
                    : ""}
                <Modal show={this.state.isOpen}
                       onClose={this.toggleModal}>

                </Modal>
            </div>
        );
    }
}

export default PostInline;