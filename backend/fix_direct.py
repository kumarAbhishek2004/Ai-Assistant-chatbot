"""
Direct database approach - update metadata with thread names
This works directly with the SQLite database
"""

import sqlite3
import json

def fix_thread_names_direct():
    print("🔧 Fixing thread names directly in database...\n")
    
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    
    # Get all threads
    cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
    threads = cursor.fetchall()
    
    print(f"Found {len(threads)} threads\n")
    
    for (thread_id,) in threads:
        print(f"\n📌 Processing: {thread_id[:20]}...")
        
        # Get the latest checkpoint for this thread to extract messages
        cursor.execute("""
            SELECT checkpoint, metadata
            FROM checkpoints
            WHERE thread_id = ?
            ORDER BY checkpoint_id DESC
            LIMIT 1
        """, (thread_id,))
        
        row = cursor.fetchone()
        if not row:
            print("  ⚠️  No checkpoints found")
            continue
        
        checkpoint_blob, metadata_blob = row
        
        # Try to extract first message from checkpoint (as JSON)
        try:
            checkpoint_str = checkpoint_blob.decode('utf-8') if isinstance(checkpoint_blob, bytes) else checkpoint_blob
            checkpoint_data = json.loads(checkpoint_str)
            
            # Look for messages
            messages = None
            if 'channel_values' in checkpoint_data and 'messages' in checkpoint_data['channel_values']:
                messages = checkpoint_data['channel_values']['messages']
            elif 'messages' in checkpoint_data:
                messages = checkpoint_data['messages']
            
            if not messages:
                print("  ⚠️  No messages found")
                continue
            
            # Find first human message
            first_human = None
            for msg in messages:
                if isinstance(msg, dict):
                    msg_type = msg.get('type', '')
                    if msg_type == 'human':
                        content = msg.get('content') or msg.get('data', {}).get('content', '')
                        if content:
                            first_human = content
                            break
            
            if not first_human:
                print("  ⚠️  No human messages found")
                continue
            
            # Create thread name
            new_name = first_human[:50] + "..." if len(first_human) > 50 else first_human
            print(f"  📝 Name: {new_name[:60]}")
            
            # Update metadata with the name
            # Parse existing metadata
            try:
                if metadata_blob:
                    metadata_str = metadata_blob.decode('utf-8') if isinstance(metadata_blob, bytes) else metadata_blob
                    metadata = json.loads(metadata_str)
                else:
                    metadata = {}
            except:
                metadata = {}
            
            # Add name to metadata
            if 'configurable' not in metadata:
                metadata['configurable'] = {}
            metadata['configurable']['name'] = new_name
            
            # Update ALL checkpoints for this thread
            new_metadata_str = json.dumps(metadata)
            cursor.execute("""
                UPDATE checkpoints
                SET metadata = ?
                WHERE thread_id = ?
            """, (new_metadata_str, thread_id))
            
            print(f"  ✅ Updated!")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 70)
    print("✨ Done! Restart your backend and refresh browser.")
    print("=" * 70)

if __name__ == "__main__":
    fix_thread_names_direct()
