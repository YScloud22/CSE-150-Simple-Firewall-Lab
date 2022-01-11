# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.
    ICMP = packet.find('icmp')
    ARP = packet.find('arp') 
    TCP = packet.find('tcp')
    IPV4 = packet.find('ipv4')
    ser1 = packet.find('20.1.1.1')
    ser2 = packet.find('20.1.1.2')
    c1 = packet.find('20.1.1.10')
    c2 = packet.find('20.1.1.11')


    if ICMP and IPV4:
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 50
      msg.hard_timeout = 50
      msg.priority = 1
      msg.buffer_id = packet_in.buffer_id
      msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      self.connection.send(msg)
    
    elif ARP:
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 50
      msg.hard_timeout = 50
      msg.priority = 2
      msg.buffer_id = packet_in.buffer_id
      msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      self.connection.send(msg)

    elif ser1 and c1 and TCP:
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 50
      msg.hard_timeout = 50
      msg.priority = 3
      msg.buffer_id = packet_in.buffer_id
      msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      self.connection.send(msg)

    elif ser2 and c2 and TCP:
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 50
      msg.hard_timeout = 50
      msg.priority = 4
      msg.buffer_id = packet_in.buffer_id
      msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      self.connection.send(msg)

    elif IPV4: #drop packet
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 50
      msg.hard_timeout = 50
      msg.buffer_id = packet_in.buffer_id
      msg.priority = 5
      self.connection.send(msg)



    #print "Example Code."

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
