#ifndef ADDITIONAL_LOGGER_ROS_H
#define ADDITIONAL_LOGGER_ROS_H

#include <rclcpp/rclcpp.hpp>
#include <xscommon/additionalloggerbase.h>

class AdditionalLoggerRos : public AdditionalLoggerBase
{
public:
  AdditionalLoggerRos(rclcpp::Logger);
  virtual ~AdditionalLoggerRos();

  void log(
    JournalLogLevel level, char const * file, int line, char const * function,
    std::string const & msg) override;

private:
  rclcpp::Logger m_ros_logger;
};

#endif
