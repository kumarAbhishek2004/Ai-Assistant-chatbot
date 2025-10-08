"""
Script to fix thread names for existing conversations.
This will rename all threads based on their first user message.
Run this from the backend directory.
"""

import sqlite3
import json
import pickle

def fix_thread_names():
    """Update all thread names based on first message"""
    
    print("🔄 Starting thread name fix...\n")
    
    try:
        # Connect to database
        conn = sqlite3.connect('chatbot.db', check_same_thread=False)
        cursor = conn.cursor()
        
        # Get all unique thread_ids
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        threads = cursor.fetchall()
        
        threads_updated = 0
        threads_skipped = 0
        
        for (thread_id,) in threads:
            try:
                # Get the latest checkpoint for this thread
                cursor.execute(
                    """SELECT checkpoint_id, checkpoint, metadata, config 
                       FROM checkpoints 
                       WHERE thread_id = ? 
                       ORDER BY checkpoint_id DESC 
                       LIMIT 1""",
                    (thread_id,)
                )
                result = cursor.fetchone()
                
                if not result:
                    continue
                
                checkpoint_id, checkpoint_blob, metadata_json, config_json = result
                
                # Parse config
                config = json.loads(config_json)
                current_name = config.get('configurable', {}).get('name', '')
                
                # Skip if already has a good name (not generic Chat X)
                if current_name and not current_name.startswith("Chat "):
                    threads_skipped += 1
                    print(f"⏭️  Skipped: {thread_id[:8]}... (already has name: {current_name})")
                    continue
                
                # Deserialize checkpoint to get messages
                checkpoint_data = pickle.loads(checkpoint_blob)
                messages = checkpoint_data.get('channel_values', {}).get('messages', [])
                
                if not messages:
                    threads_skipped += 1
                    print(f"⏭️  Skipped: {thread_id[:8]}... (no messages)")
                    continue
                
                # Find first human message
                first_human_message = None
                for msg in messages:
                    # Check if it's a HumanMessage
                    msg_type = type(msg).__name__
                    if msg_type == 'HumanMessage' or (hasattr(msg, 'type') and msg.type == 'human'):
                        first_human_message = msg.content
                        break
                
                if not first_human_message:
                    threads_skipped += 1
                    print(f"⏭️  Skipped: {thread_id[:8]}... (no human messages)")
                    continue
                
                # Create new name from first message
                new_name = first_human_message[:50] + "..." if len(first_human_message) > 50 else first_human_message
                
                # Update config
                config['configurable']['name'] = new_name
                
                # Update all checkpoints for this thread
                cursor.execute(
                    "UPDATE checkpoints SET config = ? WHERE thread_id = ?",
                    (json.dumps(config), thread_id)
                )
                
                threads_updated += 1
                print(f"✅ Updated: {thread_id[:8]}...")
                print(f"   Old name: '{current_name}'")
                print(f"   New name: '{new_name}'\n")
                
            except Exception as e:
                print(f"❌ Error processing thread {thread_id[:8]}...: {e}\n")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("\n" + "="*70)
        print(f"✨ Done! Updated {threads_updated} threads, skipped {threads_skipped}")
        print("="*70)
        print("\n🔄 Please refresh your frontend to see the changes!")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    fix_thread_names()
