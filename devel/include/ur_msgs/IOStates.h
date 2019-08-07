// Generated by gencpp from file ur_msgs/IOStates.msg
// DO NOT EDIT!


#ifndef UR_MSGS_MESSAGE_IOSTATES_H
#define UR_MSGS_MESSAGE_IOSTATES_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <ur_msgs/Digital.h>
#include <ur_msgs/Digital.h>
#include <ur_msgs/Digital.h>
#include <ur_msgs/Analog.h>
#include <ur_msgs/Analog.h>

namespace ur_msgs
{
template <class ContainerAllocator>
struct IOStates_
{
  typedef IOStates_<ContainerAllocator> Type;

  IOStates_()
    : digital_in_states()
    , digital_out_states()
    , flag_states()
    , analog_in_states()
    , analog_out_states()  {
    }
  IOStates_(const ContainerAllocator& _alloc)
    : digital_in_states(_alloc)
    , digital_out_states(_alloc)
    , flag_states(_alloc)
    , analog_in_states(_alloc)
    , analog_out_states(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector< ::ur_msgs::Digital_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::ur_msgs::Digital_<ContainerAllocator> >::other >  _digital_in_states_type;
  _digital_in_states_type digital_in_states;

   typedef std::vector< ::ur_msgs::Digital_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::ur_msgs::Digital_<ContainerAllocator> >::other >  _digital_out_states_type;
  _digital_out_states_type digital_out_states;

   typedef std::vector< ::ur_msgs::Digital_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::ur_msgs::Digital_<ContainerAllocator> >::other >  _flag_states_type;
  _flag_states_type flag_states;

   typedef std::vector< ::ur_msgs::Analog_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::ur_msgs::Analog_<ContainerAllocator> >::other >  _analog_in_states_type;
  _analog_in_states_type analog_in_states;

   typedef std::vector< ::ur_msgs::Analog_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::ur_msgs::Analog_<ContainerAllocator> >::other >  _analog_out_states_type;
  _analog_out_states_type analog_out_states;





  typedef boost::shared_ptr< ::ur_msgs::IOStates_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ur_msgs::IOStates_<ContainerAllocator> const> ConstPtr;

}; // struct IOStates_

typedef ::ur_msgs::IOStates_<std::allocator<void> > IOStates;

typedef boost::shared_ptr< ::ur_msgs::IOStates > IOStatesPtr;
typedef boost::shared_ptr< ::ur_msgs::IOStates const> IOStatesConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ur_msgs::IOStates_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ur_msgs::IOStates_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace ur_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'ur_msgs': ['/home/casch/ws_moveit/src/universal_robot-melodic-devel/ur_msgs/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::ur_msgs::IOStates_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ur_msgs::IOStates_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ur_msgs::IOStates_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ur_msgs::IOStates_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ur_msgs::IOStates_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ur_msgs::IOStates_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ur_msgs::IOStates_<ContainerAllocator> >
{
  static const char* value()
  {
    return "0a5c7b73e3189e9a2caf8583d1bae2e2";
  }

  static const char* value(const ::ur_msgs::IOStates_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x0a5c7b73e3189e9aULL;
  static const uint64_t static_value2 = 0x2caf8583d1bae2e2ULL;
};

template<class ContainerAllocator>
struct DataType< ::ur_msgs::IOStates_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ur_msgs/IOStates";
  }

  static const char* value(const ::ur_msgs::IOStates_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ur_msgs::IOStates_<ContainerAllocator> >
{
  static const char* value()
  {
    return "Digital[] digital_in_states\n"
"Digital[] digital_out_states\n"
"Digital[] flag_states\n"
"Analog[] analog_in_states\n"
"Analog[] analog_out_states\n"
"\n"
"================================================================================\n"
"MSG: ur_msgs/Digital\n"
"uint8 pin\n"
"bool state\n"
"\n"
"================================================================================\n"
"MSG: ur_msgs/Analog\n"
"uint8 pin\n"
"float32 state\n"
;
  }

  static const char* value(const ::ur_msgs::IOStates_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ur_msgs::IOStates_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.digital_in_states);
      stream.next(m.digital_out_states);
      stream.next(m.flag_states);
      stream.next(m.analog_in_states);
      stream.next(m.analog_out_states);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct IOStates_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ur_msgs::IOStates_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ur_msgs::IOStates_<ContainerAllocator>& v)
  {
    s << indent << "digital_in_states[]" << std::endl;
    for (size_t i = 0; i < v.digital_in_states.size(); ++i)
    {
      s << indent << "  digital_in_states[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::ur_msgs::Digital_<ContainerAllocator> >::stream(s, indent + "    ", v.digital_in_states[i]);
    }
    s << indent << "digital_out_states[]" << std::endl;
    for (size_t i = 0; i < v.digital_out_states.size(); ++i)
    {
      s << indent << "  digital_out_states[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::ur_msgs::Digital_<ContainerAllocator> >::stream(s, indent + "    ", v.digital_out_states[i]);
    }
    s << indent << "flag_states[]" << std::endl;
    for (size_t i = 0; i < v.flag_states.size(); ++i)
    {
      s << indent << "  flag_states[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::ur_msgs::Digital_<ContainerAllocator> >::stream(s, indent + "    ", v.flag_states[i]);
    }
    s << indent << "analog_in_states[]" << std::endl;
    for (size_t i = 0; i < v.analog_in_states.size(); ++i)
    {
      s << indent << "  analog_in_states[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::ur_msgs::Analog_<ContainerAllocator> >::stream(s, indent + "    ", v.analog_in_states[i]);
    }
    s << indent << "analog_out_states[]" << std::endl;
    for (size_t i = 0; i < v.analog_out_states.size(); ++i)
    {
      s << indent << "  analog_out_states[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::ur_msgs::Analog_<ContainerAllocator> >::stream(s, indent + "    ", v.analog_out_states[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // UR_MSGS_MESSAGE_IOSTATES_H
