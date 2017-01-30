import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

class node{
	
	String state;
	String parent;
	int path_cost;
	int depth;

	public node(String state, String parent, int path_cost, int depth){
		
		this.state = state;
		this.parent = parent;
		this.path_cost = path_cost;
		this.depth = depth;
	}
}

class input_node{
	
	String state;
	int path_cost;

	public input_node(String state, int path_cost){
		
		this.state = state;
		this.path_cost = path_cost;
	}
}
public class homework {
	
	FileReader fr;
	
	BufferedReader br;
		
	String line = null;
	
	String start_state = null, goal_state = null , algo = null;
	
	String state1, state2; 
	
	String live_traffic_lines, sunday_traffic_lines;
	
	StringTokenizer st;
	
	Map<String, Integer> sunday_map = new HashMap<String, Integer>();
	
	Map<Integer, String> map1 = new HashMap<Integer, String>();
	
	Map<String, ArrayList<input_node>> input_map = new HashMap<String, ArrayList<input_node>>();
	
	
	int no_of_live_lines = 0, input_travel_time, no_of_sunday_lines = 0;
	
	ArrayList<node> frontier;
	
	ArrayList<node> explored_set;

	public static void main(String[] str) throws java.lang.Exception{
		
		homework s= new homework();
		
		s.organizeInput();
		
		s.generalSearch();
	}

	//Reads input from file and stores values in corresponding variables
	public void organizeInput() throws IOException, FileNotFoundException{
		
		fr = new FileReader("input.txt");
		
		BufferedReader br = new BufferedReader(fr);
		
		if ( (line = br.readLine()) != null){
			
			algo = line.trim();
			
		}
		
		if ( (line = br.readLine()) != null){
			
			start_state = line.trim();
			
		}
		
		if ( (line = br.readLine()) != null){
			
			goal_state = line.trim();
			
		}
		
		if ( (line = br.readLine()) != null){
			
			try{
				no_of_live_lines = Integer.parseInt(line.trim());
			}
			catch(NumberFormatException n){
				System.out.println("Provide Correct Format");
			}
			
		}
		
		for(int k = 1; k <= no_of_live_lines ; k++){
			
			if ( (line = br.readLine()) != null){
				
				live_traffic_lines = line.trim();
				
				st = new StringTokenizer(live_traffic_lines, " ");
				
				state1 = st.nextToken();

				state2 = st.nextToken();
				
				input_travel_time = Integer.parseInt(st.nextToken());
						
				
				if( !input_map.containsKey(state1)){
					
					input_map.put(state1, new ArrayList<input_node>());
					
					input_map.get(state1).add(new input_node(state2,input_travel_time));
					
				}
				else{
					input_map.get(state1).add(new input_node(state2,input_travel_time));
				}
				
			}
		}
		
		if ( (line = br.readLine()) != null){
			
			try{
				no_of_sunday_lines = Integer.parseInt(line.trim());
			}
			catch(NumberFormatException n){
				System.out.println("Provide Correct Format");
			}
			
		}
		
		for(int k = 1; k <= no_of_sunday_lines ; k++){
			
			if ( (line = br.readLine()) != null){
				
				sunday_traffic_lines = line.trim();
				
				st = new StringTokenizer(sunday_traffic_lines, " ");
				
				state1 = st.nextToken();
				
				input_travel_time = Integer.parseInt(st.nextToken());
				
				sunday_map.put(state1, input_travel_time);
			}
		}
	}
	
  //Writes output to file
	void output(ArrayList<node> final_sol) throws IOException{
		
		FileWriter writer = new FileWriter("output.txt");
		
		BufferedWriter bw = new BufferedWriter(writer);
		
		for(int k = final_sol.size() - 1; k >= 0; k-- ){
			
			System.out.println(final_sol.get(k).state+" "+final_sol.get(k).path_cost);
			
			bw.write(final_sol.get(k).state+" "+final_sol.get(k).path_cost);
			
			bw.newLine();
		}
		
		bw.close();
		
	}
	
  //Implements search
	void generalSearch() throws NullPointerException, IOException{
		
		node n;
		
		ArrayList<node> final_sol;
		
		makeQueue(algo);
		
		explored_set = new ArrayList<node>();
		
		while(!frontier.isEmpty()){
			
			n = removeFirst();
			
			if(goalTest(n)){
				
				final_sol = solution(n) ;
				
				output(final_sol);
				
				return ;
				
			}
			
			insert(explored_set, n);
			
			node n2,n3;
			
			int j;
			
			ArrayList<node> temp = new ArrayList<node>();
			
			for(node n1: expand(n)){
				
				for(j = 0; j < explored_set.size(); j++){
					
					n2 = explored_set.get(j);
					
					if(n1.state.equals(n2.state)){
						
						if(algo.equals("BFS")||algo.equals("DFS"))
							break;
						else if(algo.equalsIgnoreCase("UCS")){
							if(n1.path_cost < n2.path_cost){
								
								explored_set.remove(j);
								temp.add(n1);
								
							}
							break;
						}	
					}
				}
				
				if(j == explored_set.size()){
					
					if(frontier.isEmpty()){

						temp.add(n1);
//						insert(frontier,n1,algo);

					}
					else{
						
						for(j = 0; j < frontier.size(); j++){
						    
							n3 = frontier.get(j);
							
						    if(n1.state.equals(n3.state)){
								
						    	if(algo.equals("BFS")||algo.equals("DFS"))
									break;
								else if(algo.equalsIgnoreCase("UCS")){

									if(n1.path_cost < n3.path_cost){
										frontier.remove(j);
										temp.add(n1);
										
									}
									break;
								}
						    	
							}
						}
						if(j == frontier.size()){
							
							temp.add(n1);

						}
					}
					
				}
			}
			
			insert(frontier,temp,algo);
			
		}
		
		
	}
	
	void makeQueue(String algo){
		
		frontier = new ArrayList<node>();
		
		if(algo.equals("A*")){
			frontier.add(new node(start_state ,"NULL", sunday_map.get(start_state), 0));
		}
		else{
			frontier.add(new node(start_state ,"NULL", 0, 0));
		}
		
	}
	
	node removeFirst(){
		
		return frontier.remove(0);
	}
	
	boolean isQueueEmpty(ArrayList<node> n){
		
		return n.isEmpty();
	}
	
	void insert(ArrayList<node> a,node n)throws NullPointerException{
		
		a.add(n);
	}
	
	void insert(ArrayList<node> a,ArrayList<node> temp,String algo)throws NullPointerException{
  
		if(algo.equals("BFS"))
			a.addAll(temp);
		else if(algo.equals("DFS")){
			
			if(a.isEmpty()){
				a.addAll(temp);
			}
				
			else
				a.addAll(0, temp);
		}
		else if(algo.equals("UCS")||algo.equals("A*")){
			
			a.addAll(temp);
			Collections.sort(a, new Comparator<node>(){
				   public int compare(node n1, node n2){
				       return n1.path_cost - n2.path_cost;
				   }
			});
		}
	}
	//Checks if goal is reached
	boolean goalTest(node n){
		
		if(n.state.equals(goal_state))
			return true;
		return false;
	}
	//Expands a node
	ArrayList<node> expand(node n){
		
		ArrayList<node> expanded_list = new ArrayList<node>();
		
		if(!input_map.containsKey(n.state)) return expanded_list;
		
		ArrayList<input_node> neighbors = input_map.get(n.state);
		
		for(int k = 0; k < neighbors.size(); k++){
			
			if(algo.equals("BFS")||algo.equals("DFS"))
				insert(expanded_list,new node(neighbors.get(k).state,n.state,n.path_cost+1,n.depth+1));
        
			else if(algo.equals("UCS"))
				insert(expanded_list,new node(neighbors.get(k).state,n.state,n.path_cost+neighbors.get(k).path_cost,n.depth+1));
        
			else
				insert(expanded_list,new node(neighbors.get(k).state,n.state,n.path_cost+neighbors.get(k).path_cost+sunday_map.get(neighbors.get(k).state),n.depth+1));
		
		}
		return expanded_list;
	}
	//Returns all the nodes visited in an order
	ArrayList<node> solution(node n){
		
		ArrayList<node> final_states = new ArrayList<node>();
		
		String state;
		
		final_states.add(n);
		
		state = n.parent;
		
		for(int p = explored_set.size() - 1; !state.equals("NULL"); p--){
			
			n = explored_set.get(p);
			
			if(n.state.equals(state)){
				
				final_states.add(n);
				
				state = n.parent;
			}
		}
		
		return final_states;
	}
	
}
