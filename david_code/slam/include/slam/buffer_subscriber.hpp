#ifndef BUFFER_SUBSCRIBER_HPP_
#define BUFFER_SUBSCRIBER_HPP_

#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"

template<typename MessageT>
class MsgSubscriber{
public:
    // cppcheck-suppress unknownMacro
    RCLCPP_SMART_PTR_DEFINITIONS(MsgSubscriber<MessageT>)

    MsgSubscriber(rclcpp::Node * const parent, std::string const & topic_name, rclcpp::QoS const & qos){
    	parent_ = parent;
    	latest_msg_time_ = rclcpp::Time(0, 0, RCL_CLOCK_UNINITIALIZED);

    	subscription_ = parent->create_subscription<MessageT>(topic_name, qos, [this](const typename MessageT::SharedPtr msg) {on_msg_received(msg);});
    }

    typename MessageT::SharedPtr take(){
        auto msg = last_received_msg_;
        last_received_msg_ = nullptr;
        return msg;
    }

    bool has_seen_msg(){
	return has_seen_msg_;
    }

    bool has_msg(){
    	return last_received_msg_ != nullptr;
    }

    rclcpp::Time latest_msg_time(){
    	return latest_msg_time_;
    }

    [[nodiscard]] typename MessageT::SharedPtr last_received_msg() const{
    	return last_received_msg_;
    }

private:
    bool has_seen_msg_{};
    rclcpp::Time latest_msg_time_;
    rclcpp::Node * parent_;

    typename MessageT::SharedPtr last_received_msg_;
    typename rclcpp::Subscription<MessageT>::SharedPtr subscription_;

    void on_msg_received(const typename MessageT::SharedPtr msg){
    	has_seen_msg_ = true;
    	last_received_msg_ = msg;
    	latest_msg_time_ = parent_->now();
    }
};

template<class MsgT, class NodeT>
void subscribe_from(
  NodeT * this_ptr,
  typename std::shared_ptr<rclcpp::Subscription<MsgT>> & subscriber,
  const std::string & topic_name,
  void (NodeT::* callback)(typename std::shared_ptr<MsgT>),
  const rclcpp::QoS & qos = rclcpp::SensorDataQoS())
{
  subscriber =
    static_cast<rclcpp::Node *>(this_ptr)->create_subscription<MsgT>(
    topic_name, qos,
    std::bind(callback, this_ptr, std::placeholders::_1));
}

template<class MsgT>
void subscribe_from(
  rclcpp::Node * const parent,
  typename std::unique_ptr<MsgSubscriber<MsgT>> & subscriber,
  const std::string & topic_name,
  const rclcpp::QoS & qos = rclcpp::SensorDataQoS())
{
  subscriber = std::make_unique<MsgSubscriber<MsgT>>(parent, topic_name, qos);
}



#endif  // BUFFER_SUBSCRIBER_HPP_
