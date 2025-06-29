#!/usr/bin/env python3
"""
Script to fix f-string backslash issues in backend/api.py
"""

import re

def fix_fstrings():
    with open('backend/api.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace problematic f-strings with string concatenation
    patterns = [
        (r'insights \+= f"🌟 I\'ve noticed joy has been a constant companion in your life lately\. That\'s beautiful! Your recent entry about \"\{recent_text\}\" shows this positive energy\. When joy flows naturally like this, it often means you\'re aligned with what truly matters to you\. Consider what\'s been fueling this happiness - maybe it\'s certain activities, people, or moments of achievement\?\n\n"', 
         'insights += "🌟 I\'ve noticed joy has been a constant companion in your life lately. That\'s beautiful! Your recent entry about \\"" + recent_text + "\\" shows this positive energy. When joy flows naturally like this, it often means you\'re aligned with what truly matters to you. Consider what\'s been fueling this happiness - maybe it\'s certain activities, people, or moments of achievement?\n\n"'),
        
        (r'insights \+= f"💙 I see sadness has been present in your journey\. Your recent reflection about \"\{recent_text\}\" touches on this\. Remember, feeling sad doesn\'t mean you\'re doing anything wrong - it\'s a natural part of being human\. Sometimes sadness is our heart\'s way of processing change or loss\. What would feel most supportive to you right now\?\n\n"',
         'insights += "💙 I see sadness has been present in your journey. Your recent reflection about \\"" + recent_text + "\\" touches on this. Remember, feeling sad doesn\'t mean you\'re doing anything wrong - it\'s a natural part of being human. Sometimes sadness is our heart\'s way of processing change or loss. What would feel most supportive to you right now?\n\n"'),
        
        (r'insights \+= f"🔥 Anger has been showing up in your entries, including your recent thoughts about \"\{recent_text\}\"\. Anger often signals that something important to you feels threatened or unfair\. It can be a powerful catalyst for change when channeled mindfully\. What might your anger be trying to tell you about your needs or boundaries\?\n\n"',
         'insights += "🔥 Anger has been showing up in your entries, including your recent thoughts about \\"" + recent_text + "\\". Anger often signals that something important to you feels threatened or unfair. It can be a powerful catalyst for change when channeled mindfully. What might your anger be trying to tell you about your needs or boundaries?\n\n"'),
        
        (r'insights \+= f"😰 I\'ve noticed fear and anxiety appearing in your reflections, like in your recent entry about \"\{recent_text\}\"\. These feelings are incredibly common and often arise when we\'re facing uncertainty or change\. Your brain is trying to protect you, even if it feels overwhelming\. What small steps could help you feel more grounded\?\n\n"',
         'insights += "😰 I\'ve noticed fear and anxiety appearing in your reflections, like in your recent entry about \\"" + recent_text + "\\". These feelings are incredibly common and often arise when we\'re facing uncertainty or change. Your brain is trying to protect you, even if it feels overwhelming. What small steps could help you feel more grounded?\n\n"'),
        
        (r'insights \+= f"😲 Your emotional landscape has been full of surprises! Your recent reflection about \"\{recent_text\}\" captures this sense of the unexpected\. Life has been throwing you curveballs, and you\'re navigating them with curiosity\. This adaptability is a real strength - you\'re learning to dance with uncertainty\.\n\n"',
         'insights += "😲 Your emotional landscape has been full of surprises! Your recent reflection about \\"" + recent_text + "\\" captures this sense of the unexpected. Life has been throwing you curveballs, and you\'re navigating them with curiosity. This adaptability is a real strength - you\'re learning to dance with uncertainty.\n\n"'),
        
        (r'insights \+= f"🤢 I see disgust has been present in your journey, including your recent thoughts about \"\{recent_text\}\"\. This emotion often arises when something feels fundamentally wrong or out of alignment with your values\. It might be signaling that certain aspects of your life need attention or change\.\n\n"',
         'insights += "🤢 I see disgust has been present in your journey, including your recent thoughts about \\"" + recent_text + "\\". This emotion often arises when something feels fundamentally wrong or out of alignment with your values. It might be signaling that certain aspects of your life need attention or change.\n\n"'),
        
        (r'insights \+= f"❤️ Love has been flowing through your entries! Your recent reflection about \"\{recent_text\}\" radiates this warmth\. When love is your dominant emotion, it often means you\'re deeply connected to what matters most\. This connection is precious - how can you nurture it further\?\n\n"',
         'insights += "❤️ Love has been flowing through your entries! Your recent reflection about \\"" + recent_text + "\\" radiates this warmth. When love is your dominant emotion, it often means you\'re deeply connected to what matters most. This connection is precious - how can you nurture it further?\n\n"'),
        
        (r'insights \+= f"😐 I\'ve noticed you\'ve been in a more neutral space lately, including your recent entry about \"\{recent_text\}\"\. Sometimes this calm center is exactly what we need - a place to rest and reset\. It can also be a sign that you\'re processing deeper emotions beneath the surface\.\n\n"',
         'insights += "😐 I\'ve noticed you\'ve been in a more neutral space lately, including your recent entry about \\"" + recent_text + "\\". Sometimes this calm center is exactly what we need - a place to rest and reset. It can also be a sign that you\'re processing deeper emotions beneath the surface.\n\n"')
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    with open('backend/api.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed all f-string backslash issues!")

if __name__ == "__main__":
    fix_fstrings() 