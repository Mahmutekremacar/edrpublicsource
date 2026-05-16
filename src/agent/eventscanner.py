import win32evtlog
import xml.etree.ElementTree as ET

class EventCollector:
    def __init__(self):
        """
        Initializes the collector and tracks the last processed record ID.
        """
        self.log_path = 'Microsoft-Windows-Sysmon/Operational'
        self.ns = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
        self.last_record_id = 0

    def get_recent_events(self, max_events=50):
        """
        Queries the Windows Event Log and extracts only new events.
        based on the last seen RecordId.
        """
        extracted_data = []
        try:
            query_handle = win32evtlog.EvtQuery(self.log_path, 513)
            events = win32evtlog.EvtNext(query_handle, max_events)
            
            if not events:
                return []

            batch_data = []

            for event in events:
                xml_content = win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml)
                root = ET.fromstring(xml_content)
                
                system_node = root.find('.//ns:System', self.ns)
                current_record_id = int(system_node.find('ns:EventRecordID', self.ns).text)

                if current_record_id <= self.last_record_id:
                    break

                event_id = root.find('.//ns:EventID', self.ns).text
                time_created_el = root.find('.//ns:TimeCreated', self.ns)
                timestamp = time_created_el.get('SystemTime') if time_created_el is not None else "Unknown"
                
                data_points = {}
                for data in root.findall('.//ns:Data', self.ns):
                    name = data.get('Name')
                    data_points[name if name else "Detail"] = data.text
                
                batch_data.append({
                    "event_type": "sysmon",
                    "record_id": current_record_id,
                    "event_id": str(event_id),
                    "timestamp": str(timestamp),
                    "EventData": data_points
                })

            if batch_data:
                self.last_record_id = max(item["record_id"] for item in batch_data)
                
                extracted_data = batch_data[::-1]
            
        except Exception as e:
            print(f"Collector Error: {e}")
            
        return extracted_data