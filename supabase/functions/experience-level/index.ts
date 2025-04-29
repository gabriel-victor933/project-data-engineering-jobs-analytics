// Setup type definitions for built-in Supabase Runtime APIs
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import express from "npm:express@4.18.2";
import { z, ZodError } from "https://deno.land/x/zod@v3.22.2/mod.ts";
const app = express();
app.use(express.json());

const experience_schema = z.object({
  level: z.string().max(64),
  description: z.string()
})

const experience_array = z.array(experience_schema)

app.post('/experience-level', async (req, res)=>{
  try {
    const experience = req.body;
  
    experience_array.parse(experience)
  
    return res.send('Experience Level Saved');
    
  } catch (error) {
    if(error instanceof ZodError){
      return res.status(400).send(error)
    }

    return res.status(500).send('error')
  }
});
app.listen(8000);
