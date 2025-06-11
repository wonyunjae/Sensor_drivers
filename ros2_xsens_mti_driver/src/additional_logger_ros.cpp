#include "additional_logger_ros.hpp"

AdditionalLoggerRos::AdditionalLoggerRos(rclcpp::Logger ros_logger)
: AdditionalLoggerBase(JLL_Trace),
  m_ros_logger(ros_logger)
{
}

AdditionalLoggerRos::~AdditionalLoggerRos()
{
}

void AdditionalLoggerRos::log(
  JournalLogLevel level, char const * file, int line, char const * function,
  std::string const & msg)
{
  switch (level) {
    case JLL_Trace:
    case JLL_Debug:
      RCLCPP_DEBUG_STREAM(m_ros_logger, file << ":" << line << " " << function << " : " << msg);
      break;

    case JLL_Alert:
    case JLL_Error:
    case JLL_Fatal:
      RCLCPP_ERROR_STREAM(m_ros_logger, file << ":" << line << " " << function << " : " << msg);
      break;

    case JLL_Write:
    case JLL_Disable:
    default:
      RCLCPP_INFO_STREAM(
        m_ros_logger,
        "level=" << level << file << ":" << line << " " << function << " : " <<
          msg);
      break;
  }
}

/// End of logger!
