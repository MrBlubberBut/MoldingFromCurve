# MoldingFromCurve
Blender addon that makes a molding from a curve

![demo_moldtocurve](https://user-images.githubusercontent.com/54787701/147623451-76a96502-c588-413c-aedd-8cd00270c38e.gif)

## Installing the addon

Download the moldingfromcurve.py file and install that as an addon in Blender by going into **Preferences --> Add-ons --> Install** and then select the file, and enable it.

## Using the addon

First, you need a curve object. It must be a mesh, however, not an actual curve. You can convert it to a curve by going into **Object --> Convert --> Mesh**. Once you have that, you need a planar object to convert the curve into. You can use an ordinary plane, or a custom one. The mesh must be completely flat.

Then, select the curve first, then Shift select the mesh, and press the big **Move mesh to curve** button. Then play with the scale, or rotation, flip it (or don't) and then finally press the big **Molding from mesh** button.

## Using my addon vs Blender built in tools

Only use my addon if you need straight corners with NO distortion using curves that use all 3 dimensions.

Therefore... if you need this:

![image](https://user-images.githubusercontent.com/54787701/147624624-bc47fb89-3c21-4bad-a49c-8dabd4912199.png)

Or this:

![image](https://user-images.githubusercontent.com/54787701/147624657-324d237b-5dac-4af6-8052-7320887fa871.png)
(Notice the curvy, not straight, corners.)

Use Blenders tools instead for stuff like that.

However, if you need straight corners with no bevelling and they must have 0 distortion, AND the curve uses all 3 dimensions, then use my addon.

![image](https://user-images.githubusercontent.com/54787701/147624767-93561054-5fe2-4402-993d-a269f35aa4aa.png)

## Why doesn't it look right?

If you're getting something like this:

![image](https://user-images.githubusercontent.com/54787701/147624809-91ad76c5-1fbd-4f2d-b3af-1c9bc443ac24.png)

Then you probably did something like this:

![image](https://user-images.githubusercontent.com/54787701/147624868-7555d1d1-f436-40cd-9c72-58ede11a2c78.png)

Notice how you go from a non-90 degree UP turn, to a 90-degree RIGHT turn. You cannot do that. If you want to turn directions, it must be a turn from a PREVIOUS 90 degree turn. Here is what it would look like fixed:

![image](https://user-images.githubusercontent.com/54787701/147624968-ad2621ea-f2c5-4c0f-a27d-02307959f6de.png)

Here's what the first, wrong example looks like if you were to do it in real life:

![image](https://user-images.githubusercontent.com/54787701/147626066-21a56464-b9ab-4d84-8606-eaddfc9971ea.png)

Notice how, in order to complete the turn, it first goes straight, and then does the turn, instead of going straight into it without correcting. So yes, I could code something like that, sure. But I don't want to.

Alternatively, here's what it would look like if you did it manually in 3D:

![image](https://user-images.githubusercontent.com/54787701/147625486-a50c07ac-2486-4dd7-bcc3-4e69739c2438.png)

Seems all well and good, right? But look closer:

![image](https://user-images.githubusercontent.com/54787701/147625430-fd3247a1-87c4-4c85-9d6a-2e56a51cf3c2.png)

Notice theres extra stuff around the mesh which I pointed to. Also notice how the face isn't a square as it should be. So, there's distortion. And that would take way too long to code for me if I actually wanted to deal with something like that.


## Why is it so slow?

Me bad at code. If you want to make it faster, feel free to change the script, or make your own. Or don't. I don't care. 
If you do have a big curve and a big mesh with both having lots of vertices, just give it time. Wait a few minutes if necessary, it'll work. I promise. Or maybe it won't. That could happen too.
