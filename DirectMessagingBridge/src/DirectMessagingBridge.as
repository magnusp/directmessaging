package
{
	import flash.display.Sprite;
	import flash.external.ExternalInterface;
	import flash.system.Security;
	
	import org.codehaus.stomp.Stomp;
	import org.codehaus.stomp.event.ConnectedEvent;
	import org.codehaus.stomp.event.MessageEvent;
	
	public class DirectMessagingBridge extends Sprite
	{
		private var stomp:Stomp = new Stomp();
		private var brokerhost:String;
		private var policyserveruri:String;
		private var brokerport:uint;
		
		public function DirectMessagingBridge()
		{
			if(ExternalInterface.available) {
				policyserveruri = stage.loaderInfo.parameters.policyserveruri;
				brokerhost = stage.loaderInfo.parameters.brokerhost;
				brokerport = uint(stage.loaderInfo.parameters.brokerport);
				
				Security.loadPolicyFile(policyserveruri);
				stomp.addEventListener(ConnectedEvent.CONNECTED, onConnected);
				stomp.connect(brokerhost, brokerport);
			} else {
				// Do something here
			}
		}
		
		private function onConnected(event:ConnectedEvent):void {
			ExternalInterface.addCallback("directmessaging_send", onWebWorldSend);
			stomp.subscribe("/topic/directmessaging-outgoing");
			stomp.addEventListener(MessageEvent.MESSAGE, onMessage);
		}
		
		private function onMessage(event:MessageEvent):void {
			ExternalInterface.call("messageCallback", event.message.body.toString());
		}
		
		private function onWebWorldSend(thing:String):void {
			stomp.sendTextMessage("/queue/directmessaging-incoming", thing);
		}
	}
}